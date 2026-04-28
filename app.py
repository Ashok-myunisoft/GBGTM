# ==========================================
# app.py
# GoodBooks Mock MCP Server
# Full Fixed Version
# ==========================================

from fastmcp import FastMCP

# ==================================================
# MOCK HRMS
# ==================================================

from mock_service.mock_hrms import (
    apply_leave,
    leave_balance,
    attendance_summary
)

# ==================================================
# MOCK PROCUREMENT
# ==================================================

from mock_service.mock_procurement import (
    create_purchase_order
)

# ==================================================
# MOCK FINANCE
# ==================================================

from mock_service.mock_finance import (
    ledger_balance,
    invoice_status,
    expense_claim
)

# ==================================================
# MOCK INVENTORY
# ==================================================

from mock_service.mock_inventory import (
    stock_check,
    item_details,
    low_stock_items
)

# ==================================================
# MCP APP
# ==================================================

mcp = FastMCP("goodbooks-erp")


# ==================================================
# HRMS TOOLS
# ==================================================

@mcp.tool()
def leave_balance_tool():
    """Get employee leave balance"""
    return leave_balance()


@mcp.tool()
def apply_leave_tool(
    leave_type: str,
    leave_date: str,
    reason: str = ""
):
    """Apply leave request"""
    return apply_leave({
        "leave_type": leave_type,
        "leave_date": leave_date,
        "reason": reason
    })


@mcp.tool()
def attendance_summary_tool():
    """Get attendance summary"""
    return attendance_summary()


# ==================================================
# PROCUREMENT TOOLS
# ==================================================

@mcp.tool()
def create_purchase_order_tool(
    vendor_id: str,
    item_id: str,
    quantity: float,
    unit_price: float
):
    """Create purchase order"""

    return create_purchase_order({
        "vendor_id": vendor_id,
        "item_id": item_id,
        "quantity": quantity,
        "unit_price": unit_price
    })


# ==================================================
# FINANCE TOOLS
# ==================================================

@mcp.tool()
def ledger_balance_tool(ledger_id: str):
    """Get ledger balance"""
    return ledger_balance(ledger_id)


@mcp.tool()
def invoice_status_tool(invoice_no: str):
    """Get invoice payment status"""
    return invoice_status(invoice_no)

@mcp.tool()
def expense_claim_tool(
    claim_type: str,
    amount: float,
    remarks: str = ""
):
    """
    Submit expense claim
    """

    return expense_claim(
        claim_type=claim_type,
        amount=amount,
        remarks=remarks
    )


# ==================================================
# INVENTORY TOOLS
# ==================================================

@mcp.tool()
def stock_check_tool(item_id: str):
    """Check stock"""
    return stock_check(item_id)


@mcp.tool()
def item_details_tool(item_id: str):
    """Get item details"""
    return item_details(item_id)


@mcp.tool()
def low_stock_items_tool(
    warehouse: str = "",
    threshold: int = 5
):
    """
    Get low stock items by warehouse
    """

    return low_stock_items(
        warehouse=warehouse,
        threshold=threshold
    )


# ==================================================
# RUN SERVER
# ==================================================

if __name__ == "__main__":

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8007,
        path="/mcp"
    )