// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Sales Order"] = {
	fields:  ["delivery_date", "end_date", "status", "customer_name", "name"],
	field_map: {
		"start": "delivery_date",
		"end": "end_date",
		"id": "name",
		"title": "title",
		"allDay": "allDay"
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "customer",
			"options": "Customer",
			"label": __("Customer")
		},
		{
			"fieldtype": "Select",
			"fieldname": "delivery_status",
			"options": "Not Delivered\nFully Delivered\nPartly Delivered\nClosed\nNot Applicable",
			"label": __("Delivery Status")
		},
		{
			"fieldtype": "Select",
			"fieldname": "billing_status",
			"options": "Not Billed\nFully Billed\nPartly Billed\nClosed",
			"label": __("Billing Status")
		},
		{
			"fieldtype": "Select",
			"fieldname": "delivery_date",
			"label": __("Delivery Date")
		},
		{
			"fieldtype": "Select",
			"fieldname": "end_date",
			"label": __("End Date")
		},
	],
	get_events_method: "erpnext.selling.doctype.sales_order.sales_order.get_events",
	get_css_class: function(data) {
		if(data.status=="Closed") {
			return "success";
		} if(data.delivery_status=="Not Delivered") {
			return "danger";
		} else if(data.delivery_status=="Partly Delivered") {
			return "warning";
		} else if(data.delivery_status=="Fully Delivered") {
			return "success";
		}
	}
}
