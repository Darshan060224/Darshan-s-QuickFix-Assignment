# Copyright (c) 2026, darshan's and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		settings = frappe.get_single("QuickFix Settings")
		if not self.labour_charge:
			self.labour_charge = settings.default_labour_charge
