import frappe
import json
import frappe.utils
from frappe import _
from frappe.contacts.doctype.address.address import get_company_address
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html


@frappe.whitelist()
def make_purchase_order_for_default_supplier(source_name, selected_items=None, target_doc=None,supplier=None):
	"""Creates Purchase Order for each Supplier. Returns a list of doc objects."""
	if not selected_items:
		return

	if isinstance(selected_items, str):
		selected_items = json.loads(selected_items)

	def set_missing_values(source, target):
		target.supplier = supplier
		target.apply_discount_on = ""
		target.additional_discount_percentage = 0.0
		target.discount_amount = 0.0
		target.inter_company_order_reference = ""

		default_price_list = frappe.get_value("Supplier", supplier, "default_price_list")
		if default_price_list:
			target.buying_price_list = default_price_list

		if any(item.delivered_by_supplier == 1 for item in source.items):
			if source.shipping_address_name:
				target.shipping_address = source.shipping_address_name
				target.shipping_address_display = source.shipping_address
			else:
				target.shipping_address = source.customer_address
				target.shipping_address_display = source.address_display

			target.customer_contact_person = source.contact_person
			target.customer_contact_display = source.contact_display
			target.customer_contact_mobile = source.contact_mobile
			target.customer_contact_email = source.contact_email

		else:
			target.customer = ""
			target.customer_name = ""

		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item(source, target, source_parent):
		target.schedule_date = source.delivery_date
		target.qty = flt(source.qty) - (flt(source.ordered_qty) / flt(source.conversion_factor))
		target.stock_qty = flt(source.stock_qty) - flt(source.ordered_qty)
		target.project = source_parent.project

	suppliers = [item.get("supplier") for item in selected_items if item.get("supplier")]
	suppliers = list(dict.fromkeys(suppliers))  # remove duplicates while preserving order

	items_to_map = [item.get("item_code") for item in selected_items if item.get("item_code")]
	items_to_map = list(set(items_to_map))

	if not suppliers:
		frappe.throw(
			_("Please set a Supplier against the Items to be considered in the Purchase Order.")
		)

	purchase_orders = []
	for supplier in suppliers:
		doc = get_mapped_doc(
			"Sales Order",
			source_name,
			{
				"Sales Order": {
					"doctype": "Purchase Order",
					"field_no_map": [
						"address_display",
						"contact_display",
						"contact_mobile",
						"contact_email",
						"contact_person",
						"taxes_and_charges",
						"shipping_address",
						"terms",
					],
					"validation": {"docstatus": ["=", 1]},
				},
				"Sales Order Item": {
					"doctype": "Purchase Order Item",
					"field_map": [
						["name", "sales_order_item"],
						["parent", "sales_order"],
						["stock_uom", "stock_uom"],
						["uom", "uom"],
						["conversion_factor", "conversion_factor"],
						["delivery_date", "schedule_date"],
					],
					"field_no_map": [
						"rate",
						"price_list_rate",
						"item_tax_template",
						"discount_percentage",
						"discount_amount",
						"pricing_rules",
					],
					"postprocess": update_item,
					"condition": lambda doc: doc.ordered_qty < doc.stock_qty
					and doc.supplier == supplier
					and doc.item_code in items_to_map,
				},
			},
			target_doc,
			set_missing_values,
		)

		doc.insert()
		frappe.db.commit()
		purchase_orders.append(doc)

	return purchase_orders


@frappe.whitelist()
def make_purchase_order(source_name, selected_items=None, target_doc=None,po_supplier=None):
	if not selected_items:
		return

	if isinstance(selected_items, str):
		selected_items = json.loads(selected_items)

	def set_missing_values(source, target):
		target.supplier = po_supplier
		target.apply_discount_on = ""
		target.additional_discount_percentage = 0.0
		target.discount_amount = 0.0
		target.inter_company_order_reference = ""
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")

	def update_item(source, target, source_parent):
		target.schedule_date = source.delivery_date
		target.qty = flt(source.qty) - (flt(source.ordered_qty) / flt(source.conversion_factor))
		target.stock_qty = flt(source.stock_qty) - flt(source.ordered_qty)
		target.project = source_parent.project

	suppliers = [item.get("po_supplier") for item in selected_items if item.get("po_supplier")]
	suppliers = list(dict.fromkeys(suppliers))  # remove duplicates while preserving order

	items_to_map = [item.get("item_code") for item in selected_items if item.get("item_code")]
	items_to_map = list(set(items_to_map))

	if not suppliers:
		frappe.throw(
			_("Please set a Supplier against the Items to be considered in the Purchase Order.")
		)

	purchase_orders = []
	for po_supplier in suppliers:
		doc = get_mapped_doc(
			"Sales Order",
			source_name,
			{
				"Sales Order": {
					"doctype": "Purchase Order",
					"field_no_map": [
						"address_display",
						"contact_display",
						"contact_mobile",
						"contact_email",
						"contact_person",
						"taxes_and_charges",
						"shipping_address",
						"terms",
					],
					"validation": {"docstatus": ["=", 1]},
				},
				"Sales Order Item": {
					"doctype": "Purchase Order Item",
					"field_map": [
						["name", "sales_order_item"],
						["parent", "sales_order"],
						["stock_uom", "stock_uom"],
						["uom", "uom"],
						["conversion_factor", "conversion_factor"],
						["delivery_date", "schedule_date"],
					],
					"field_no_map": [
						"rate",
						"price_list_rate",
						"item_tax_template",
						"discount_percentage",
						"discount_amount",
						"pricing_rules",
					],
					"postprocess": update_item,
					"condition": lambda doc: doc.ordered_qty < doc.stock_qty
					and doc.po_supplier == po_supplier
					and doc.item_code in items_to_map,
				},
			},
			target_doc,
			set_missing_values,
		)
		
		doc.insert()
		frappe.db.commit()
		purchase_orders.append(doc)
		print("-------->",purchase_orders)

	return purchase_orders


def set_delivery_date(items, sales_order):
	delivery_dates = frappe.get_all(
		"Sales Order Item", filters={"parent": sales_order}, fields=["delivery_date", "item_code"]
	)

	delivery_by_item = frappe._dict()
	for date in delivery_dates:
		delivery_by_item[date.item_code] = date.delivery_date