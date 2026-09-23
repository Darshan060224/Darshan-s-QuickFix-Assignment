# B2c — Dangerous Patterns

    given code:
        def validate(self):
        self.total = sum(r.amount for r in self.items)
        self.save()
        other = frappe.get_doc("Spare Part", self.part)
        other.stock_qty -= self.qty
        other.save()
    Bug-1:
        self.save() is not need in this place why it is recalling  inside the validate function
        correct code:
            def validate(self):
                self.total = sum(r.amount for r in self.items)
            reason:This part is fine for this to do the validation process
    Bug-2:
        inside Validate Function need to do calculation
        Correct code:
            def validate(self):
                self.total = sum(r.amount for r in self.items)
                other = frappe.get_doc("Spare Part", self.part)
                other.save()

# B2d — Concurrency, One Question:

    the reason for Document cant be modified after you have opened it because dont let the  old record cant modify the new record in frappe there i an concept called optimistic locking it help to prevent like things

# C3 Part Usage Entry & Service Invoice:

    when the user changes the Technician record example assigned_technician the associated linked record are also change. this is why that "merge=false" is used here

# D2 Row-Level Filtering & Data Leak:

    The reason why frappe.get_all is dangarous because it ignore the permissions and that return all in the dict format so it is dangerous inplaces like this we can use get_list() for safe purpose
# E1:
    i tried to call self.save() inside on_update it recursely calls on_update and goes on infinitely 

# E2 — Autoname and Renaming
    the reason of using merge=false if it is not  it will merge the  new name to that existing name so we use that.

# E3 — One Performance Judgment Call
    threshold = frappe.db.get_value(
    "QuickFix Settings",
    None,
    "low_stock_threshold"
    )
    Need full document Means frappe.get_doc()
    Need one value means frappe.db.get_value()

    