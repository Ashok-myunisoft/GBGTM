from fastmcp import FastMCP
from auth.login_context import parse_login
from services.hrms_services import (
    leave_balance,
    apply_leave,
    apply_permission
)

mcp = FastMCP("GoodBooks-MCP")


@mcp.tool()
def leave_balance_tool(login_dto):
    login = parse_login(login_dto)
    return leave_balance(login)


@mcp.tool()
def apply_leave_tool(
    login_dto,
    leave_type,
    leave_date,
    reason
):
    login = parse_login(login_dto)

    return apply_leave(
        login,
        leave_type,
        leave_date,
        reason
    )


@mcp.tool()
def apply_permission_tool(
    login_dto,
    shift_id,
    shift_name,
    department_name,
    designation_name,
    date,
    from_time,
    to_time,
    reason
):
    login = parse_login(login_dto)

    return apply_permission(
        login,
        shift_id,
        shift_name,
        department_name,
        designation_name,
        date,
        from_time,
        to_time,
        reason
    )
