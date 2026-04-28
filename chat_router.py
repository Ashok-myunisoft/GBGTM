# ==========================================
# COMPLETE SOLUTION
# chat_router.py
# GoodBooks AI Tool Router
# User Question -> Correct MCP Tool
# ==========================================

import re
from datetime import datetime, timedelta


# ==================================================
# MAIN ROUTER
# ==================================================

def route_query(message: str):

    msg = message.lower().strip()

    # ==================================================
    # LEAVE BALANCE
    # ==================================================

    if "leave balance" in msg or "my leave" in msg:

        return {
            "tool": "leave_balance_tool",
            "arguments": {}
        }

    # ==================================================
    # APPLY LEAVE
    # ==================================================

    elif "apply leave" in msg or "need leave" in msg:

        date = extract_date(msg)

        reason = extract_reason(msg)

        return {
            "tool": "apply_leave_tool",
            "arguments": {
                "leave_type": "Casual Leave",
                "leave_date": date,
                "reason": reason
            }
        }

    # ==================================================
    # ATTENDANCE
    # ==================================================

    elif "attendance" in msg:

        return {
            "tool": "attendance_summary_tool",
            "arguments": {}
        }

    # ==================================================
    # PURCHASE ORDER
    # ==================================================

    elif "purchase order" in msg or "create po" in msg:

        return {
            "tool": "create_purchase_order_tool",
            "arguments": {
                "vendor_id": "V001",
                "item_id": "I001",
                "quantity": 10,
                "unit_price": 2500
            }
        }

    # ==================================================
    # LEDGER BALANCE
    # ==================================================

    elif "ledger" in msg:

        return {
            "tool": "ledger_balance_tool",
            "arguments": {
                "ledger_id": "L001"
            }
        }

    # ==================================================
    # INVOICE STATUS
    # ==================================================

    elif "invoice" in msg:

        inv = extract_invoice(msg)

        return {
            "tool": "invoice_status_tool",
            "arguments": {
                "invoice_no": inv
            }
        }

    # ==================================================
    # STOCK CHECK
    # ==================================================

    elif "stock" in msg:

        return {
            "tool": "stock_check_tool",
            "arguments": {
                "item_id": "ITM001"
            }
        }

    # ==================================================
    # LOW STOCK
    # ==================================================

    elif "low stock" in msg:

        return {
            "tool": "low_stock_items_tool",
            "arguments": {}
        }

    # ==================================================
    # EXPENSE CLAIM
    # ==================================================

    elif "expense" in msg:

        return {
            "tool": "expense_claim_tool",
            "arguments": {
                "claim_type": "Travel",
                "amount": 2500,
                "remarks": "Client Visit"
            }
        }

    # ==================================================
    # DEFAULT
    # ==================================================

    return {
        "tool": None,
        "arguments": {},
        "message": "No matching tool found"
    }


# ==================================================
# DATE EXTRACTOR
# ==================================================

def extract_date(msg):

    today = datetime.today()

    if "tomorrow" in msg:
        return (
            today + timedelta(days=1)
        ).strftime("%Y-%m-%d")

    elif "today" in msg:
        return today.strftime("%Y-%m-%d")

    # YYYY-MM-DD
    m = re.search(
        r"\d{4}-\d{2}-\d{2}",
        msg
    )

    if m:
        return m.group()

    return today.strftime("%Y-%m-%d")


# ==================================================
# REASON EXTRACTOR
# ==================================================

def extract_reason(msg):

    if "fever" in msg:
        return "Fever"

    elif "personal" in msg:
        return "Personal Work"

    elif "sick" in msg:
        return "Sick"

    return "General Request"


# ==================================================
# INVOICE EXTRACTOR
# ==================================================

def extract_invoice(msg):

    m = re.search(
        r"inv[- ]?\d+",
        msg
    )

    if m:
        return m.group().upper()

    return "INV-1001"