# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalesOrderTimesheetDetail(Document):
	pass

@frappe.whitelist()
def sort_so_time_logs(ts):
    so_tls = frappe.db.get_list('Sales Order Timesheet Detail', {'timesheet': ts}, ['start_datetime', 'end_datetime', 'name'])
    sso_tls = sorted(so_tls, key=lambda item: (item['start_datetime'], item['end_datetime']))
    n = 1
    for so_tl in sso_tls:
        frappe.db.set_value('Sales Order Timesheet Detail', so_tl['name'], 'idx', n)
        n += 1

@frappe.whitelist()
def delete_old_so_time_log(ts):
    so_tls = frappe.db.get_list('Sales Order Timesheet Detail', {'timesheet': ts}, ['name', 'time_log_name'])
    for so_tl in so_tls:
        if not frappe.db.exists('Timesheet Detail', so_tl['time_log_name']):
            frappe.delete_doc('Sales Order Timesheet Detail', so_tl['name'])

@frappe.whitelist()
def insert_so_time_log(tl_name):
    so_tl_name = frappe.db.get_value('Sales Order Timesheet Detail', {'time_log_name': tl_name}, 'name')
    tl = frappe.db.get_value('Timesheet Detail', tl_name, ['parent', 'activity_type', 'from_time', 'to_time', 'hours', 'description', 'sales_order'], as_dict=1)
    timesheet = frappe.db.get_value('Timesheet', tl['parent'], ['employee', 'employee_name'], as_dict=1)
    if so_tl_name and tl['sales_order']:
        frappe.db.set_value('Sales Order Timesheet Detail', so_tl_name, {
            'parent': tl['sales_order'],
            'parenttype': 'Sales Order',
            'parentfield': 'working_team',
            'timesheet': tl['parent'],
            'employee': timesheet['employee'],
            'employee_name': timesheet['employee_name'],
#            'time_log_name': tl['name'],
            'activity_type': tl['activity_type'],
            'start_datetime': tl['from_time'],
            'end_datetime': tl['to_time'],
            'hours': tl['hours'],
            'description': tl['description']
            })
    elif tl['sales_order']:
        ntl = frappe.get_doc({
            'doctype': 'Sales Order Timesheet Detail',
            'parent': tl['sales_order'],
            'parenttype': 'Sales Order',
            'parentfield': 'working_team',
            'timesheet': tl['parent'],
            'employee': timesheet['employee'],
            'employee_name': timesheet['employee_name'],
            'time_log_name': tl_name,
            'activity_type': tl['activity_type'],
            'start_datetime': tl['from_time'],
            'end_datetime': tl['to_time'],
            'hours': tl['hours'],
            'description': tl['description']
            })
        ntl.insert()
    else:
        frappe.delete_doc('Sales Order Timesheet Detail', so_tl_name)


@frappe.whitelist()
def get_so_details(so):
    details = frappe.get_value(
            "Sales Order",
            so,
            ['shipping_address_name', 'shipping_address', 'delivery_date', 'end_date'],
            as_dict=1
            )
    return details
