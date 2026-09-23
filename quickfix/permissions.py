import frappe


def job_card_query(user):
    if "QF Technician" in frappe.get_roles(user):
        return f"""
            `tabJob Card`.assigned_technician IN (
                SELECT name
                FROM `tabTechnician`
                WHERE user = {frappe.db.escape(user)}
            )
        """
    return ""