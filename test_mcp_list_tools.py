#!/usr/bin/env python3
"""
Test MCP server with tools/list handler.
"""

import asyncio
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mcp.server import Server
from mcp.types import Tool, TextContent, CallToolRequest, CallToolResult, ListToolsRequest, ListToolsResult
import mcp.server.stdio


# Create server
app = Server("test-server")


# Define a simple tool handler
async def handle_test_tool(ctx, params: CallToolRequest) -> CallToolResult:
    """Handle test tool calls."""
    print(f"Tool call received: {params}", file=sys.stderr)
    
    # Extract tool name and arguments
    tool_name = params.name
    arguments = params.arguments or {}
    
    if tool_name == "test_tool":
        query = arguments.get("query", "")
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"✅ Test tool called with query: {query}"
                )
            ],
            isError=False
        )
    else:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"❌ Tool not found: {tool_name}"
                )
            ],
            isError=True
        )


# Define tools list handler
async def handle_list_tools(ctx, params: ListToolsRequest) -> ListToolsResult:
    """Handle tools/list requests."""
    print(f"List tools request received", file=sys.stderr)
    
    # Define available tools
    tools = [
        Tool(
            name="test_tool",
            description="A test tool that echoes back the query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to echo back"
                    }
                },
                "required": ["query"]
            }
        )
    ]
    
    return ListToolsResult(tools=tools)


# Register the handlers
try:
    # Register tools/call handler
    app.add_request_handler(
        method="tools/call",
        params_type=CallToolRequest,
        handler=handle_test_tool
    )
    print("✅ Registered tools/call handler", file=sys.stderr)
    
    # Register tools/list handler
    app.add_request_handler(
        method="tools/list",
        params_type=ListToolsRequest,
        handler=handle_list_tools
    )
    print("✅ Registered tools/list handler", file=sys.stderr)
    
except Exception as e:
    print(f"❌ Error registering handlers: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()


async def main():
    """Test MCP server."""
    print("🚀 Testing MCP server...", file=sys.stderr)
    
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            print("✅ stdio server created", file=sys.stderr)
            
            # Try to run
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
            
    except Exception as e:
        print(f"❌ Error running server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())