# Copyright (c) 2026, darshan's and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		if not self.customer_phone or not self.customer_phone.isdigit() or len(self.customer_phone) != 10:
			frappe.throw("Enter the customer phone number correctly")
		if self.status in ["In Repair", "Ready for Delivery", "Delivered"] and not self.assigned_technician:
			frappe.throw("Assigned Technician is required for this status")
		
		if self.status == "Ready for Delivery":
			if not frappe.db.exists("QA Check", {"job_card": self.name, "final_verdict": "Pass"}):
				frappe.throw("do QA check")
		self.parts_total = 0
		for row in self.parts_used:
			row.total_price = row.quantity * row.unit_price
			self.parts_total += row.total_price
		if not self.labour_charge:
			settings = frappe.get_single("QuickFix Settings")
			self.labour_charge = settings.default_labour_charge
		self.final_amount = self.labour_charge + self.parts_total
	def on_submit(self):
		for row in self.parts_used:
			stock_qty=frappe.db.get_value("Spare Part",row.part,"stock_qty")
			frappe.db.set_value("Spare Part",row.part,"stock_qty",stock_qty-row.quantity,ignore_permissions=True)
		invoice = frappe.get_doc({
			"doctype": "Service Invoice",
			"job_card": self.name,
			"labour_charge": self.labour_charge,
			"parts_total": self.parts_total,
			"total_amount": self.final_amount,
			"payment_status": "Unpaid"
		})
		invoice.insert()
		frappe.enqueue("quickfix.tasks.send_job_ready_email",job_card_name=self.name)
	def before_submit(self):
		if self.status != "Ready for Delivery":frappe.throw("Job Card can only be submitted when status is Ready for Delivery.")
		for row in self.parts_used:
			stock_qty = frappe.db.get_value("Spare Part",row.part,"stock_qty")
			if stock_qty < row.quantity:frappe.throw(f"Insufficient stock for {row.part}. "f"Available: {stock_qty}, Required: {row.quantity}")
	def on_cancel(self):
		if self.status=="Cancelled":
			for row in self.parts_used:
				stock_qty = frappe.db.get_value("Spare Part",row.part,"stock_qty")
				frappe.db.set_value("Spare Part",row.part,"stock_qty",stock_qty + row.quantity,ignore_permissions=True)
			invoice_name = frappe.db.get_value("Service Invoice",{"job_card": self.name},"name")
		if invoice_name:
			invoice = frappe.get_doc("Service Invoice",invoice_name)
			if invoice.docstatus == 1:
				invoice.cancel()
	def on_trash(self):
		if self.status not in ["Cancelled","Draft"]:
			frappe.throw("Job Card cannot be trashed.")

	def before_print(self, print_settings=None):
		self.print_summary = f"{self.customer_name or ''}, {self.device_brand or ''}, {self.device_model or ''}"		