frappe.views.calendar["Timesheet"] = {
	field_map: {
		"start": "start_date",
		"end": "end_date",
		"name": "parent",
		"id": "name",
		"allDay": "allDay",
		"child_name": "name",
		"title": "title"
	},
	style_map: {
		"0": "info",
		"1": "standard",
		"2": "danger"
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "project",
			"options": "Project",
			"label": __("Project")
		},
		{
			"fieldtype": "Link",
			"fieldname": "employee",
			"options": "Employee",
			"label": __("Employee")
		},
		{
			"fieldtype": "Link",
			"fieldname": "sales_order",
			"options": "Sales Order",
			"label": __("Sales Order")
		}
	],
	get_events_method: "erpnext.projects.doctype.timesheet.timesheet.get_events",
	get_css_class: function(data) {
		if(data.status=="Draft") {
			return "danger";
                } else if(data.status=="Sent") {
			return "warning";
		} else if(data.status=="Submitted") {
			return "info";
		} else if(data.status=="Billed") {
			return "success";
		}
	}
}
