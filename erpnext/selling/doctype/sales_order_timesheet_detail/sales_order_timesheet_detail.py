# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalesOrderTimesheetDetail(Document):
	pass

@frappe.whitelist()
def get_so_time_logs(so):
    time_logs = frappe.get_list(
            "Timesheet Detail",
            filters={ 'sales_order': so },
            fields=['activity_type','from_time','to_time', 'hours', 'description', 'parent']
            )
    for time_log in time_logs:
        time_log['employee'] = frappe.db.get_value('Timesheet', time_log['parent'], 'employee')
        time_log['employee_name'] = frappe.db.get_value('Timesheet', time_log['parent'], 'employee_name')
    return time_logs

@frappe.whitelist()
def get_so_details(so):
    details = frappe.get_value(
            "Sales Order",
            so,
            ['shipping_address_name', 'shipping_address', 'delivery_date', 'end_date'],
            as_dict=1
            )
    return details
