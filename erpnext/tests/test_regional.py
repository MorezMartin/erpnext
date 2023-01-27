import unittest

import frappe

import erpnext


@erpnext.allow_regional
def test_method():
	return "original"


class TestInit(unittest.TestCase):
	def test_regional_overrides(self):
<<<<<<< HEAD
		frappe.flags.country = "India"
		self.assertEqual(test_method(), "overridden")

		frappe.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")

=======
		frappe.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")

>>>>>>> 3967773fbeddfd05b53f722f1b51ea813a57b3c1
		frappe.flags.country = "France"
		self.assertEqual(test_method(), "overridden")
