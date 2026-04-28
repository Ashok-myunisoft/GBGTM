import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import Client
from chat_router import route_query

APP_MCP_URL = os.getenv(
    "APP_MCP_URL",
    "http://127.0.0.1:8007/mcp"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mcp_client = Client(APP_MCP_URL)
    yield


app = FastAPI(
    title="GoodBooks Frontend API",
    version="1.0",
    lifespan=lifespan
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
async def chat(payload: dict):

    user_msg = payload["message"]

    route = route_query(user_msg)

    tool = route["tool"]
    args = route["arguments"]

    if tool is None:
        return {
            "status": "error",
            "message": route["message"]
        }

    try:
        client = app.state.mcp_client

        async with client:
            result = await client.call_tool(tool, args)

        if result.is_error:
            return {
                "status": "error",
                "message": "Tool execution failed",
                "tool": tool
            }

        if result.data is not None:
            return result.data

        if result.structured_content is not None:
            return result.structured_content

        if result.content:
            first = result.content[0]
            return {
                "status": "success",
                "message": getattr(first, "text", str(first))
            }

        return {
            "status": "success",
            "tool": tool
        }

    except Exception as e:
        raise HTTPException(500, str(e))

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
            "stock_check",
            "low_stock_items",
            "expense_claim"
        ]
    }


# ==========================================
# HRMS
# ==========================================

@app.post("/apply-leave")
async def api_apply_leave(payload: dict):

    try:
        async with app.state.mcp_client as client:
            result = await client.call_tool(
                "apply_leave_tool",
                {
                    "leave_type": payload["leave_type"],
                    "leave_date": payload["leave_date"],
                    "reason": payload.get("reason", "")
                }
            )
        return result.data or result.structured_content or {}

    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/leave-balance")
async def api_leave_balance():

    async with app.state.mcp_client as client:
        result = await client.call_tool("leave_balance_tool", {})
    return result.data or result.structured_content or {}


@app.get("/attendance-summary")
async def api_attendance():

    async with app.state.mcp_client as client:
        result = await client.call_tool("attendance_summary_tool", {})
    return result.data or result.structured_content or {}


# ==========================================
# PROCUREMENT
# ==========================================

@app.post("/create-po")
async def api_create_po(payload: dict):

    try:
        async with app.state.mcp_client as client:
            result = await client.call_tool(
                "create_purchase_order_tool",
                {
                    "vendor_id": payload["vendor_id"],
                    "item_id": payload["item_id"],
                    "quantity": payload["quantity"],
                    "unit_price": payload["unit_price"]
                }
            )
        return result.data or result.structured_content or {}

    except Exception as e:
        raise HTTPException(500, str(e))


# ==========================================
# FINANCE
# ==========================================

@app.get("/ledger-balance/{ledger_id}")
async def api_ledger_balance(ledger_id: str):

    async with app.state.mcp_client as client:
        result = await client.call_tool("ledger_balance_tool", {"ledger_id": ledger_id})
    return result.data or result.structured_content or {}


@app.get("/invoice-status/{invoice_no}")
async def api_invoice_status(invoice_no: str):

    async with app.state.mcp_client as client:
        result = await client.call_tool("invoice_status_tool", {"invoice_no": invoice_no})
    return result.data or result.structured_content or {}


# ==========================================
# INVENTORY
# ==========================================

@app.get("/stock-check/{item_id}")
async def api_stock_check(item_id: str):

    async with app.state.mcp_client as client:
        result = await client.call_tool("stock_check_tool", {"item_id": item_id})
    return result.data or result.structured_content or {}
