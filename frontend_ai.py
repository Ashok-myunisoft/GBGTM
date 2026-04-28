# ==========================================
# frontend_api.py
# Frontend REST API for GoodBooks MCP Tools
# Run:
# uvicorn frontend_api:app --reload --port 9000
# ==========================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chat_router import route_query

# MOCK SERVICES
from mock_service.mock_hrms import (
    apply_leave,
    leave_balance,
    attendance_summary
)

from mock_service.mock_procurement import (
    create_purchase_order
)

from mock_service.mock_finance import (
    ledger_balance,
    invoice_status,
    expense_claim
)

from mock_service.mock_inventory import (
    stock_check,
    low_stock_items
)

app = FastAPI(
    title="GoodBooks Frontend API",
    version="1.0"
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "*" ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# HEALTH
# ==========================================

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "GoodBooks Frontend API Running"
    }

@app.post("/chat")
def chat(payload: dict):

    user_msg = payload["message"]

    route = route_query(user_msg)

    tool = route["tool"]
    args = route["arguments"]

    if tool == "leave_balance_tool":
        return leave_balance()

    elif tool == "apply_leave_tool":
        return apply_leave(args)

    elif tool == "attendance_summary_tool":
        return attendance_summary()

    elif tool == "create_purchase_order_tool":
        return create_purchase_order(args)

    elif tool == "ledger_balance_tool":
        return ledger_balance(args["ledger_id"])

    elif tool == "invoice_status_tool":
        return invoice_status(args["invoice_no"])

    elif tool == "stock_check_tool":
        return stock_check(args["item_id"])

    elif tool == "low_stock_items_tool":
        return low_stock_items()

    elif tool == "expense_claim_tool":
        return expense_claim(
            args["claim_type"],
            args["amount"],
            args["remarks"]
        )

    return {
        "status": "error",
        "message": "No tool matched"
    }
# ==========================================
# TOOL LIST
# ==========================================

@app.get("/tools")
def tools():

    return {
        "tools": [
            "apply_leave",
            "leave_balance",
            "attendance_summary",
            "create_purchase_order",
            "ledger_balance",
            "invoice_status",
            "stock_check"
        ]
    }


# ==========================================
# HRMS
# ==========================================

@app.post("/apply-leave")
def api_apply_leave(payload: dict):

    try:
        return apply_leave({
            "leave_type": payload["leave_type"],
            "leave_date": payload["leave_date"],
            "reason": payload.get("reason", "")
        })

    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/leave-balance")
def api_leave_balance():

    return leave_balance()


@app.get("/attendance-summary")
def api_attendance():

    return attendance_summary()


# ==========================================
# PROCUREMENT
# ==========================================

@app.post("/create-po")
def api_create_po(payload: dict):

    try:
        return create_purchase_order({
            "vendor_id": payload["vendor_id"],
            "item_id": payload["item_id"],
            "quantity": payload["quantity"],
            "unit_price": payload["unit_price"]
        })

    except Exception as e:
        raise HTTPException(500, str(e))


# ==========================================
# FINANCE
# ==========================================

@app.get("/ledger-balance/{ledger_id}")
def api_ledger_balance(ledger_id: str):

    return ledger_balance(ledger_id)


@app.get("/invoice-status/{invoice_no}")
def api_invoice_status(invoice_no: str):

    return invoice_status(invoice_no)


# ==========================================
# INVENTORY
# ==========================================

@app.get("/stock-check/{item_id}")
def api_stock_check(item_id: str):

    return stock_check(item_id)