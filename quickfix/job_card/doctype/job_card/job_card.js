// Copyright (c) 2026, darshan's and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	setup(frm) {
		frm.set_query("assigned_technician", () => {
			return {
				filters: {
					status: "Active",
					specialization: frm.doc.device_type,
				}
			};
		});
	},
	refresh(frm) {
    frm.dashboard.add_indicator(frm.doc.status);
    if (frm.doc.status === "Ready for Delivery" && frm.doc.docstatus === 1) {
        frm.add_custom_button("Mark as Delivered", function () {
            frm.set_value("status", "Delivered");
            frm.save();
        });
    }
}
});
