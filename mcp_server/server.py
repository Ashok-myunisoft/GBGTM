from mcp.server import Server

from mcp_server.registry import TOOLS
from mcp_server.dispatcher import dispatch_tool


server = Server("goodbooks-erp")


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(
    name,
    arguments,
    ctx
):
    return await dispatch_tool(
        name,
        arguments,
        ctx
    )
    