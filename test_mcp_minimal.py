#!/usr/bin/env python3
"""
Minimal MCP server test.
"""

import asyncio
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mcp.server import Server
from mcp.types import Tool, TextContent, CallToolRequest, CallToolResult
import mcp.server.stdio


# Create server
app = Server("test-server")


# Define a simple tool handler
async def handle_test_tool(params: CallToolRequest) -> CallToolResult:
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


# Register the handler
try:
    # In MCP 2.x, we need to use add_request_handler with correct parameters
    # The method expects: method, params_type, handler
    
    app.add_request_handler(
        method="tools/call",
        params_type=CallToolRequest,
        handler=handle_test_tool
    )
    print("✅ Handler registered", file=sys.stderr)
    
except Exception as e:
    print(f"❌ Error registering handler: {e}", file=sys.stderr)
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