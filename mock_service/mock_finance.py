# ==========================================
# services/mock_finance.py
# GoodBooks Mock Finance Services
# ==========================================


# ==================================================
# LEDGER BALANCE
# ==================================================

def ledger_balance(ledger_id: str):

    return {
        "status": "success",
        "ledger_id": ledger_id,
        "ledger_name": "Sales Account",
        "current_balance": 245000.75,
        "currency": "INR",
        "as_on_date": "2026-04-25"
    }


# ==================================================
# INVOICE STATUS
# ==================================================

def invoice_status(invoice_no: str):

    return {
        "status": "success",
        "invoice_no": invoice_no,
        "customer_name": "ABC Traders",
        "invoice_amount": 78500.00,
        "paid_amount": 50000.00,
        "balance_amount": 28500.00,
        "payment_status": "Partially Paid",
        "due_date": "2026-05-10"
    }


# ==================================================
# EXPENSE CLAIM
# ==================================================

def expense_claim():

    return {
        "status": "success",
        "claim_id": "EXP-2026-103",
        "employee_name": "Ashok",
        "claim_amount": 3500,
        "claim_status": "Pending Approval"
    }