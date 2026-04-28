# ==========================================
# dispatcher.py
# GoodBooks MCP Dispatcher
# MOCK DATA VERSION
# ==========================================

import json

from mcp.types import TextContent


# ==================================================
# MOCK SERVICES
# ==================================================

from mock_service.mock_hrms import (
    apply_leave,
    leave_balance,
    apply_permission,
    attendance_summary,
    employee_profile,
    payslip
)

from mock_service.mock_procurement import (
    create_purchase_order,
    vendor_balance
)

from mock_service.mock_payroll import (
    payroll_summary,
    salary_structure
)

from mock_service.mock_finance import (
    ledger_balance,
    invoice_status
)

from mock_service.mock_inventory import (
    stock_check
)


# ==================================================
# MAIN DISPATCHER
# ==================================================

async def dispatch_tool(
    name,
    arguments,
    ctx
):

    # ==================================================
    # HRMS
    # ==================================================

    if name == "apply_leave":

        result = apply_leave(
            leave_type=arguments["leave_type"],
            leave_date=arguments["leave_date"],
            reason=arguments.get("reason", "")
        )

    elif name == "leave_balance":

        result = leave_balance()

    elif name == "apply_permission":

        result = apply_permission(
            date=arguments["date"],
            from_time=arguments["from_time"],
            to_time=arguments["to_time"],
            reason=arguments.get("reason", "")
        )

    elif name == "attendance_summary":

        result = attendance_summary()

    elif name == "employee_profile":

        result = employee_profile()

    elif name == "payslip":

        result = payslip(
            month=arguments.get("month", "")
        )

    # ==================================================
    # PROCUREMENT
    # ==================================================

    elif name == "create_purchase_order":

        result = create_purchase_order(
            vendor_id=arguments["vendor_id"],
            item_id=arguments["item_id"],
            quantity=arguments["quantity"],
            unit_price=arguments["unit_price"],
            delivery_date=arguments.get(
                "delivery_date",
                ""
            ),
            remarks=arguments.get(
                "remarks",
                ""
            )
        )

    elif name == "vendor_balance":

        result = vendor_balance(
            vendor_id=arguments["vendor_id"]
        )

    # ==================================================
    # PAYROLL
    # ==================================================

    elif name == "payroll_summary":

        result = payroll_summary()

    elif name == "salary_structure":

        result = salary_structure()

    # ==================================================
    # FINANCE
    # ==================================================

    elif name == "ledger_balance":

        result = ledger_balance(
            ledger_id=arguments["ledger_id"]
        )

    elif name == "invoice_status":

        result = invoice_status(
            invoice_no=arguments["invoice_no"]
        )

    # ==================================================
    # INVENTORY
    # ==================================================

    elif name == "stock_check":

        result = stock_check(
            item_id=arguments["item_id"]
        )

    # ==================================================
    # UNKNOWN TOOL
    # ==================================================

    else:

        result = {
            "status": "error",
            "message": f"Unknown tool: {name}"
        }

    return [
        TextContent(
            type="text",
            text=json.dumps(result)
        )
    ]