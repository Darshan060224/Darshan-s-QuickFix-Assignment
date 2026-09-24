from frappe import whitelist
import frappe
import frappe.query_builder 
from frappe.query_builder import DocType 
from frappe.utils import add_days,today,nowdate

@frappe.whitelist()
def get_over_due_jobs():
    JC=DocType("Job Card")
    due=add_days(nowdate(),-7)
    result=frappe.qb.from_(JC).select(
        JC.name,JC.customer_name,JC.assigned_technician,JC.creation
    ).where(JC.status.isin(["Pending Diagnosis","In Repair"])).where(JC.creation<due).orderby(JC.creation).run(as_dict=True)
    return result

@frappe.whitelist
def transfer_job(from_tech,to_tech):
    try:
        frappe.db.sql(
            """
            UPDATE `tabJob Card` SET assigned_technician = %s WHERE assigned_technician=%s AND  status NOT IN('Delivered','Cancelled','Completed')
            """,(to_tech,from_tech)
        )
        frappe.db.commit()
    except Exception as e:
        frappe.db.rollback()
        frappe.log.error(frappe.get_traceback("Job tranfer error"))

@frappe.whitelist()
def unsafe_job_card(job_card_name):
    doc = frappe.get_doc("Job Card", job_card_name)
    return doc.as_dict()

@frappe.whitelist()
def safe_job_card(job_card_name):
    jobs = frappe.get_list(
        "Job Card",
        filters={"name": job_card_name},
        fields=[
            "name",
            "customer_name",
            "customer_phone",
            "customer_email",
            "device_type",
            "device_brand",
            "device_model",
            "assigned_technician",
            "status",
            "estimated_cost",
            "final_amount"
        ]
    )
    job = jobs[0]
    if "QF Manager" not in frappe.get_roles(frappe.session.user):
        job.pop("customer_phone", None)
        job.pop("customer_email", None)

    return job

@frappe.whitelist()
def rename_technician(old_name, new_name):
    frappe.rename_doc("Technician", old_name, new_name, merge=False)
    frappe.db.commit()
    return f"Renamed {old_name} to {new_name}. changed sucessfully"

@frappe.whitelist()
def share_job_card(job_card_name, user_email):
    frappe.share.add(
        doctype="Job Card",
        name=job_card_name,
        user=user_email,
        read=1,
    )
    
@frappe.whitelist(allow_guest=True)
def get_job_summary():
    job_card_name = frappe.form_dict.get("job_card_name")
    if not job_card_name or not frappe.db.exists("Job Card", job_card_name):
        frappe.local.response["http_status_code"] = 404
        return {"Not found"}
    job = frappe.get_doc("Job Card", job_card_name)
    summary = {
        "name": job.name,
        "customer_name": job.customer_name,
        "status": job.status,
        "final_amount": job.final_amount
    }
    return summary
    