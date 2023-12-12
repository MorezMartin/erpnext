// Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
<<<<<<< HEAD
/* eslint-disable */
=======

>>>>>>> v15.5.0

frappe.query_reports["Warehouse Wise Stock Balance"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company")
<<<<<<< HEAD
=======
		},
		{
			"fieldname":"show_disabled_warehouses",
			"label": __("Show Disabled Warehouses"),
			"fieldtype": "Check",
			"default": 0

>>>>>>> v15.5.0
		}
	],
	"initial_depth": 3,
	"tree": true,
	"parent_field": "parent_warehouse",
	"name_field": "warehouse"
};
