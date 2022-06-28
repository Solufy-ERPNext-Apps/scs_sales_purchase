frappe.ui.form.on("Sales Order", {
	refresh: function(frm) {
		if (!frm.doc.is_internal_customer) {

			if (frm.doc.docstatus == 1){

			frm.add_custom_button(__('Purchase Order'), () => {

				let pending_items = frm.doc.items.some((item) =>{
					let pending_qty = flt(item.stock_qty) - flt(item.ordered_qty);
					return pending_qty > 0;
				})

				if(!pending_items){
					frappe.throw({message: __("Purchase Order already created for all Sales Order items"), title: __("Note")});
				}
			
				var dialog = new frappe.ui.Dialog({
					title: __("Select Items"),
					size: "large",
					fields: [
						{
							"fieldtype": "Check",
							"label": __("Against Default Supplier"),
							"fieldname": "against_default_supplier",
							"default": 0,
							"description": "If not use Against Default Supplier and if you use a <b>Custom Supplier</b>, you must click the <b>Update Custom Supplier</b>."
						},
						{
							fieldname: 'items_for_po', fieldtype: 'Table', label: 'Select Items',
							fields: [
								{
									fieldtype:'Link',
									options:'Item',
									fieldname:'item_code',
									label: __('Item'),
									in_list_view:1
								},
								{
									fieldtype:'Data',
									fieldname:'item_name',
									label: __('Item name'),
									in_list_view:0
								},
								{
									fieldtype:'Float',
									fieldname:'pending_qty',
									label: __('Pending Qty'),
									in_list_view:1
								},
								{
									fieldtype:'Link',
									options:'UOM',
									fieldname:'uom',
									label: __('UOM'),
									in_list_view:1,
								},
								{
									fieldtype:'Link',
									options:'Supplier',
									fieldname:'supplier',
									label: __('Default Supplier'),
									in_list_view:1
								},
								{
									fieldtype:'Link',
									options:'Supplier',
									fieldname:'po_supplier',
									label: __('Custom Supplier'),
									in_list_view:1,
								},
							
							]
						}
					],
					primary_action_label: 'Create Purchase Order',
					primary_action (args) {
						if (!args) return;
						let selected_items = dialog.fields_dict.items_for_po.grid.get_selected_children();
						if(selected_items.length == 0) {
							frappe.throw({message: 'Please select Items from the Table', title: __('Items Required'), indicator:'blue'})
						}
						// dialog.hide();

						var method = args.against_default_supplier ? "make_purchase_order_for_default_supplier" : "make_purchase_order"
						return frappe.call({
							method: "scs_sales_purchase.api." + method,
							freeze: true,
							freeze_message: __("Creating Purchase Order ..."),
							args: {
								"source_name": frm.doc.name,
								"selected_items": selected_items,
								"po_supplier": selected_items[0].po_supplier
							},
							freeze: true,
							callback: function(r) {
								if(!r.exc) {
									if (!args.against_default_supplier) {
										for (var i =0; i < r.message.length; i++)
										{		
											frappe.msgprint({
												title: __('Purchase Order'),
									            indicator: 'blue',
									            message: __('<a onclick="window.open(this.href);return false;" href="/app/purchase-order/' + r.message[i].name +'">' + r.message[i].name + '</a>')
									        });
										}
									}
									else {
										frappe.route_options = {
											"sales_order": frm.doc.name
										}
										for (var i =0; i < r.message.length; i++)
										{		
											frappe.msgprint({
												title: __('Purchase Order'),
									            indicator: 'blue',
									            message: __('<a onclick="window.open(this.href);return false;" href="/app/purchase-order/' + r.message[i].name +'">' + r.message[i].name + '</a>')
									        });
										}

									}
								}
							}
						})
					},
					secondary_action_label: 'Update Custom Supplier',
		            secondary_action(args) {
		            	let selected_items = dialog.fields_dict.items_for_po.grid.get_selected_children();

					    $.each(frm.doc.items, function(i, v) {
						for (var j =0; j < selected_items.length; j++)
						{
							if (v.item_code == selected_items[j].item_code){
								frappe.model.set_value(v.doctype, v.name, 'po_supplier', selected_items[j].po_supplier)
							}
						}
						frm.refresh_field('items');
						setTimeout(() => {
							frm.save("Update");
						}, 10);
					})

					}

				});

				dialog.fields_dict["against_default_supplier"].df.onchange = () => set_po_items_data(dialog);

				function set_po_items_data (dialog) {
					var against_default_supplier = dialog.get_value("against_default_supplier");
					var items_for_po = dialog.get_value("items_for_po");
					if (against_default_supplier) {
						let items_with_supplier = items_for_po.filter((item) => item.supplier)
						dialog.fields_dict["items_for_po"].df.data = items_with_supplier;
						dialog.get_field("items_for_po").refresh();

							let po_items = [];
							frm.doc.items.forEach(d => {
							let ordered_qty = d.ordered_qty
							let pending_qty = (flt(d.stock_qty) - ordered_qty) / flt(d.conversion_factor);
							if (pending_qty > 0) {
								po_items.push({
									"doctype": "Sales Order Item",
									"name": d.name,
									"item_name": d.item_name,
									"item_code": d.item_code,
									"pending_qty": pending_qty,
									"uom": d.uom,
									"supplier": d.supplier
								});
							}
						});
						dialog.fields_dict["items_for_po"].df.data = po_items;
						dialog.get_field("items_for_po").grid.only_sortable();
					} 
					else {
							let po_items = [];
							frm.doc.items.forEach(d => {
							let ordered_qty = d.ordered_qty
							let pending_qty = (flt(d.stock_qty) - ordered_qty) / flt(d.conversion_factor);
							if (pending_qty > 0) {
								po_items.push({
									"doctype": "Sales Order Item",
									"item_name": d.item_name,
									"item_code": d.item_code,
									"pending_qty": pending_qty,
									"uom": d.uom,
									"po_supplier": d.po_supplier
								});
							}
						});
						$("div[data-fieldname = item_code]").css({'pointer-events':'none'});
						$("div[data-fieldname = item_name]").css({'pointer-events':'none'});
						$("div[data-fieldname = uom]").css({'pointer-events':'none'});
						$("div[data-fieldname = pending_qty]").css({'pointer-events':'none'});
						$("div[data-fieldname = supplier]").css({'pointer-events':'none'});
						dialog.fields_dict["items_for_po"].df.data = po_items;
						dialog.get_field("items_for_po").refresh();
					}
				}
				set_po_items_data(dialog);
				dialog.get_field("items_for_po").refresh();
				// dialog.wrapper.find('.grid-heading-row .grid-row-check').click();
				dialog.show();

			}, __("Create"));
		
			}
		}
	}
});