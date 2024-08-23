# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class SalesOrderTimesheetDetail(Document):
	pass

@frappe.whitelist()
def update_sos(ts):
	so_s = frappe.db.get_all('Sales Order Timesheet Detail', {'timesheet': ts}, pluck='parent')
	sos = [frappe.get_doc('Sales Order', so) for so in so_s]
	for so in sos:
		if so.docstatus == 1:
			tl_s = frappe.db.get_all('Sales Order Timesheet Detail', {'parent': so})
			tls = [frappe.get_doc('Sales Order Timesheet Detail', tl['name']) for tl in tl_s]
			so.working_team = tls
			so.save()
			so.reload()
		if so.docstatus == 2:
			frappe.throw(_('Sales Order is canceled, please change it'))


@frappe.whitelist()
def sort_time_logs(ts):
	tls = frappe.db.get_all('Timesheet Detail', {'parent': ts}, ['from_time', 'to_time', 'name'])
	s_tls = sorted(tls, key=lambda item: (item['from_time'], item['to_time']))
	n = 1
	for s_tl in s_tls:
		frappe.db.set_value('Timesheet Detail', s_tl['name'], 'idx', n)
		n += 1

@frappe.whitelist()
def delete_old_so_time_log(ts):
	so_tls = frappe.db.get_all('Sales Order Timesheet Detail', {'timesheet': ts}, ['name', 'time_log_name', 'parent', 'docstatus'])
	sos = []
	for so_tl in so_tls:
		if not frappe.db.exists('Timesheet Detail', so_tl['time_log_name']):
			if so_tl['docstatus'] == 1:
				frappe.get_doc('Sales Order Timesheet Detail', so_tl['name']).cancel()
				frappe.delete_doc('Sales Order Timesheet Detail', so_tl['name'])
				sos.append(so_tl['parent'])
			else:
				frappe.delete_doc('Sales Order Timesheet Detail', so_tl['name'])

@frappe.whitelist()
def insert_so_time_log(tl_name):
	so_tl_name = frappe.db.get_value('Sales Order Timesheet Detail', {'time_log_name': tl_name}, 'name')
	so_tl_docstatus = frappe.db.get_value('Sales Order Timesheet Detail', {'time_log_name': tl_name}, 'docstatus')
	tl = frappe.db.get_value('Timesheet Detail', tl_name, ['parent', 'activity_type', 'from_time', 'to_time', 'hours', 'description', 'sales_order'], as_dict=1)
	timesheet = frappe.db.get_value('Timesheet', tl['parent'], ['employee', 'employee_name'], as_dict=1)
	if so_tl_name and tl['sales_order']:
		frappe.db.set_value('Sales Order Timesheet Detail', so_tl_name, {
			'parent': tl['sales_order'],
			'parenttype': 'Sales Order',
			'parentfield': 'working_team',
			'timesheet': tl['parent'],
			'time_log_name': tl_name,
			'employee': timesheet['employee'],
			'employee_name': timesheet['employee_name'],
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
			'time_log_name': tl_name,
			'employee': timesheet['employee'],
			'employee_name': timesheet['employee_name'],
			'activity_type': tl['activity_type'],
			'start_datetime': tl['from_time'],
			'end_datetime': tl['to_time'],
			'hours': tl['hours'],
			'description': tl['description']
			})
		ntl.insert()
	else:
		if so_tl_docstatus == 1:
			frappe.get_doc('Sales Order Timesheet Detail', so_tl_name).cancel()
		frappe.delete_doc('Sales Order Timesheet Detail', so_tl_name)
		frappe.db.commit()

def sort_so_time_logs(so):
	so_tls = frappe.db.get_all('Sales Order Timesheet Detail', {'parent': so}, ['start_datetime', 'end_datetime', 'name'])
	sso_tls = sorted(so_tls, key=lambda item: (item['start_datetime'], item['end_datetime']))
	n = 1
	for sso_tl in sso_tls:
		frappe.db.set_value('Sales Order Timesheet Detail', sso_tl['name'], 'idx', n)
		n += 1

@frappe.whitelist()
def get_so_details(so):
	details = frappe.get_value(
			"Sales Order",
			so,
			['shipping_address_name', 'shipping_address', 'delivery_date', 'end_date'],
			as_dict=1
			)
	return details
