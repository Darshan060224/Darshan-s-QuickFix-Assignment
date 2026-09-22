from frappe import whitelist
import frappe
import frappe.query_builder 
from frappe.query_builder import DocType 
from frappe.utils import add_days,today,nowdate

@frappe.whitelist()
def get_over_due_jobs():
    JC=DocType("Job Card")
    due=add_days(nowdate(),-1)
    result=frappe.qb.from_(JC).select(
        JC.name,JC.customer_name,JC.assigned_technician,JC.creation
    ).where(JC.status.isin(["Pending Diagnosis","In Repair"])).where(JC.delivery_date<due).run()
    return result
    