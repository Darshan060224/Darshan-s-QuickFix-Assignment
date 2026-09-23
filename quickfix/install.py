import frappe


def after_install():
    for device_type in ["Smartphone", "Laptop", "Tablet"]:
        if not frappe.db.exists("Device Type", device_type):
            frappe.get_doc({
                "doctype": "Device Type",
                "device_type": device_type
            }).insert()

    if not frappe.db.exists("QuickFix Settings", "QuickFix Settings"):
        frappe.get_doc({
            "doctype": "QuickFix Settings",
            "shop_name": "QuickFix",
            "manager_email": "darshan-owner@gmail.com",
            "default_labour_charge": 500
        }).insert()
