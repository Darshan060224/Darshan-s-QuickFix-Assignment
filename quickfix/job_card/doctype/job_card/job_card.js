// Copyright (c) 2026, darshan's and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	setup(frm) {
		frm.set_query("assigned_technician", () => {
			return {
				filters: {
					status: "Active",
					specialization: frm.doc.device_type,
				},
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
		if (frm.doc.docstatus <= 1 && frm.doc.status !== "Cancelled") {
			frm.add_custom_button("Reject Job", function () {
				let dialog = new frappe.ui.Dialog({
					title: "Reject Job",
					fields: [
						{
							label: "Rejection Reason",
							fieldname: "rejection_reason",
							fieldtype: "Small Text",
							reqd: 1,
						},
					],
					primary_action_label: "Reject",
					primary_action(values) {
						frm.set_value("status", "Cancelled");
						frm.set_value("remarks", values.rejection_reason);
						frm.save();
						dialog.hide();
					},
				});
				dialog.show();
			});
			frm.add_custom_button("Transfer Technician", function () {
				frappe.prompt(
					[
						{
							label: "Technician",
							fieldname: "technician",
							fieldtype: "Link",
							options: "Technician",
							reqd: 1,
						},
					],
					function (values) {
						frappe.confirm("technician will change it is ok foryou", function () {
							frappe.call({
								method: "quickfix.api.transfer_technician",
								args: {
									job_card: frm.doc.name,
									technician: values.technician,
								},
								callback: function () {
									frm.reload_doc();
									frm.trigger("assigned_technician");
								},
							});
						});
					},
					"Transfer Technician",
					"Transfer",
				);
			});
		}
	},
	assigned_technician(frm) {
		if (!frm.doc.assigned_technician) return;
		frappe.db.get_doc("Technician", frm.doc.assigned_technician).then((doc) => {
			if (doc.specialization !== frm.doc.device_type) {
				frappe.msgprint(
					"The assigned technician's specialization does not match for you device",
				);
			}
		});
	},
});

frappe.ui.form.on("Part Usage Entry", {
	quantity(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		row.total_price = row.quantity * row.unit_price;
		frappe.model.set_value(cdt, cdn, "total_price", row.total_price);
	},
});
