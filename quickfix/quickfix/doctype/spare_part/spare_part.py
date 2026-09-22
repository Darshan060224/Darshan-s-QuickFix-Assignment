# Copyright (c) 2026, darshan's and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):
	def autoname(self):
		if self.part_code:
			self.part_code = self.part_code.upper()
		self.name = make_autoname("PART-.YYYY.-.####")

	def validate(self):
		if self.selling_price and self.unit_cost and self.selling_price <= self.unit_cost:
			frappe.throw("Selling Price must be greater than Unit Cost.")

