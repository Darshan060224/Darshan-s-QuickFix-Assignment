import frappe
def send_job_ready_email(job_card_name):
    job = frappe.get_doc("Job Card", job_card_name)
    if job.customer_email:
        frappe.sendmail(
            recipients=[job.customer_email],
            subject="Your Device is Ready for Delivery",
            message=f"Your Job Card {job.name} is ready for delivery."
        )
        