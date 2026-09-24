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

# H1 — Job Card Form Script
   
frappe.call is asynchronous one. Its result is available only after the callback/promise completes so code in validate should not immediately depend on a value returned by frappe.call  Async validation should be handled using the appropriate callback/promise flow instead.

# I1 — Query Report: Open Job Cards
     i think the reason could be by using the f-string it directly addong the query to that funtion so any one can easily attempt sql injection so by using f-string %(variable)s if we use this we can avoid that sql injection by that "%s" string

# J1 — Job Card Receipt
     the differnce is only on rendering the print page if we use the frappe.get_all() inside the jinja template it loads it in at run time but if we use before_print() it will load it in before the print page is rendered and frappe.get() get that from db directly and  before_print() will follow doc.precomputed_fiels

# K2 — Spot the N+1
    the main is here is calling the get_doc() inside the loop is the main N+1 issue here instead of that we can use get_list()

# L1 — API Standard CRUD
**Request:**
```bash
curl -X GET "http://quickfix.local:8000/api/resource/Job%20Card/JC-2026-00001" \
     -H "Authorization: token <API_KEY>:<API_SECRET>"
```

**Response:**
```json
{
    "data": {
        "name": "JC-2026-00005",
        "owner": "Administrator",
        "creation": "2026-09-23 10:00:00.000000",
        "modified": "2026-09-24 10:00:00.000000",
        "docstatus": 0,
        "customer_name": "darshan",
        "status": "In Repair",
        "device_brand": "Apple",
        "device_model": "iPhone 13",
        "assigned_technician": "TECH-0001",
        "final_amount": 1500.0
    }
}
```
