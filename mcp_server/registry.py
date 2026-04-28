# ==========================================
# registry.py
# GoodBooks MCP Tool Registry
# Existing structure friendly
# ==========================================

from mcp.types import Tool


TOOLS = [

    # ======================================================
    # HRMS TOOLS
    # ======================================================

    Tool(
        name="apply_leave",
        description=(
            "Apply leave for logged-in employee. "
            "Creates leave request and returns status."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "leave_type": {
                    "type": "string",
                    "description": "Example: Casual Leave"
                },
                "leave_date": {
                    "type": "string",
                    "format": "date",
                    "description": "YYYY-MM-DD"
                },
                "reason": {
                    "type": "string",
                    "description": "Optional reason"
                }
            },
            "required": [
                "leave_type",
                "leave_date"
            ]
        }
    ),

    Tool(
        name="leave_balance",
        description="Get current leave balances for logged-in employee.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),

    Tool(
        name="apply_permission",
        description=(
            "Apply permission / timeslip for short leave hours."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date"
                },
                "from_time": {
                    "type": "string",
                    "description": "HH:MM"
                },
                "to_time": {
                    "type": "string",
                    "description": "HH:MM"
                },
                "reason": {
                    "type": "string"
                }
            },
            "required": [
                "date",
                "from_time",
                "to_time"
            ]
        }
    ),

    Tool(
        name="attendance_summary",
        description="Get attendance summary for logged-in employee.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),

    Tool(
        name="employee_profile",
        description="Get employee profile details.",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    ),

    Tool(
        name="payslip",
        description="Get latest payslip summary.",
        inputSchema={
            "type": "object",
            "properties": {
                "month": {
                    "type": "string",
                    "description": "Example: 2026-04"
                }
            }
        }
    ),

    # ======================================================
    # PROCUREMENT TOOLS
    # ======================================================

    Tool(
        name="create_purchase_order",
        description=(
            "Create purchase order for vendor/item."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "vendor_id": {
                    "type": "string"
                },
                "item_id": {
                    "type": "string"
                },
                "quantity": {
                    "type": "number"
                },
                "unit_price": {
                    "type": "number"
                },
                "delivery_date": {
                    "type": "string",
                    "format": "date"
                },
                "remarks": {
                    "type": "string"
                }
            },
            "required": [
                "vendor_id",
                "item_id",
                "quantity",
                "unit_price"
            ]
        }
    ),

    Tool(
        name="vendor_balance",
        description="Get vendor outstanding balance.",
        inputSchema={
            "type": "object",
            "properties": {
                "vendor_id": {
                    "type": "string"
                }
            },
            "required": ["vendor_id"]
        }
    ),

    # ======================================================
    # FINANCE TOOLS
    # ======================================================

    Tool(
        name="ledger_balance",
        description="Get ledger current balance.",
        inputSchema={
            "type": "object",
            "properties": {
                "ledger_id": {
                    "type": "string"
                }
            },
            "required": ["ledger_id"]
        }
    ),

    Tool(
        name="invoice_status",
        description="Get invoice payment status.",
        inputSchema={
            "type": "object",
            "properties": {
                "invoice_no": {
                    "type": "string"
                }
            },
            "required": ["invoice_no"]
        }
    ),

    # ======================================================
    # INVENTORY TOOLS
    # ======================================================

    Tool(
        name="stock_check",
        description="Check available stock for item.",
        inputSchema={
            "type": "object",
            "properties": {
                "item_id": {
                    "type": "string"
                }
            },
            "required": ["item_id"]
        }
    ),

]

