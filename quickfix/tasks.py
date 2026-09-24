from frappe.model import rename_doc
from frappe.utils import today
import frappe
import datetime

def send_job_ready_email(job_card_name):
    job = frappe.get_doc("Job Card", job_card_name)
    if job.customer_email:
        frappe.sendmail(
            recipients=[job.customer_email],
            subject="Your Device is Ready for Delivery",
            message=f"Your Job Card {job.name} is ready for delivery."
        )
        
def check_low_stock():
    last_run = frappe.db.get_value("Audit Log", {"action": "check_low_stock", "date": today()}, "name")
    if last_run:
        return 
    threshold = frappe.db.get_value("QuickFix Settings", None, "low_stock_threshold") or 0
    low_stock_parts = frappe.get_list("Spare Part", 
        fields=["name", "stock_qty"],
        filters={"stock_qty": ["<", threshold]},
        as_dict=True
    )
    if frappe.db.exists("DocType", "Audit Log"):
        frappe.get_doc({
            "doctype": "Audit Log",
            "action": "check_low_stock",
            "date": today(),
            "timestamp": frappe.utils.now()
        }).insert(ignore_permissions=True)
    
    
