from . import __version__ as app_version

app_name = "scs_sales_purchase"
app_title = "SCS Sales-Purchase"
app_publisher = "Nihantra Patel"
app_description = "Sales-Purchase"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "n.patel.serpentcs@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/scs_sales_purchase/css/scs_sales_purchase.css"
# app_include_js = "/assets/scs_sales_purchase/js/scs_sales_purchase.js"

# include js, css files in header of web template
# web_include_css = "/assets/scs_sales_purchase/css/scs_sales_purchase.css"
# web_include_js = "/assets/scs_sales_purchase/js/scs_sales_purchase.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "scs_sales_purchase/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}
# include js in page
# page_js = {"page" : "public/js/file.js"}


doctype_js = {
				"Sales Order" : "public/js/sales_order.js"
				}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "scs_sales_purchase.utils.jinja_methods",
# 	"filters": "scs_sales_purchase.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "scs_sales_purchase.install.before_install"
# after_install = "scs_sales_purchase.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "scs_sales_purchase.uninstall.before_uninstall"
# after_uninstall = "scs_sales_purchase.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "scs_sales_purchase.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"scs_sales_purchase.tasks.all"
# 	],
# 	"daily": [
# 		"scs_sales_purchase.tasks.daily"
# 	],
# 	"hourly": [
# 		"scs_sales_purchase.tasks.hourly"
# 	],
# 	"weekly": [
# 		"scs_sales_purchase.tasks.weekly"
# 	],
# 	"monthly": [
# 		"scs_sales_purchase.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "scs_sales_purchase.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "scs_sales_purchase.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "scs_sales_purchase.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"scs_sales_purchase.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
