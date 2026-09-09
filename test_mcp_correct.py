#!/usr/bin/env python3
"""
Test correct MCP server implementation.
"""

import asyncio
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio


# Create server
app = Server("test-server")


# Define a handler for tools/call
async def handle_tool_call(params):
    """Handle tool call requests."""
    print(f"Tool call received: {params}")
    
    # Extract tool name and arguments
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    
    if tool_name == "test_tool":
        query = arguments.get("query", "")
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"✅ Test tool called with query: {query}"
                }
            ]
        }
    else:
        return {
            "error": {
                "code": -32601,
                "message": f"Tool not found: {tool_name}"
            }
        }


# Register the handler
# In MCP 2.x, we need to use add_request_handler with correct parameters
# The method expects: method, params_type, handler

# Let's check what params_type should be
print("Checking MCP types...")
try:
    from mcp.types import CallToolRequest, CallToolResult
    print("✅ CallToolRequest and CallToolResult imported")
except Exception as e:
    print(f"❌ Error importing CallToolRequest/CallToolResult: {e}")

# Try to register the handler
try:
    # In MCP 2.x, the handler signature might be different
    # Let's check the source code
    
    import inspect
    from mcp.server.lowlevel.server import Server as LowLevelServer
    
    # Get the add_request_handler method
    method = getattr(LowLevelServer, 'add_request_handler')
    sig = inspect.signature(method)
    
    print(f"\nadd_request_handler signature: {sig}")
    
    # Check the handler type
    handler_param = sig.parameters.get('handler')
    if handler_param:
        print(f"Handler annotation: {handler_param.annotation}")
        
        # Try to get the actual type
        try:
            from mcp.types import RequestHandler
            print(f"RequestHandler type: {RequestHandler}")
        except Exception as e:
            print(f"Error importing RequestHandler: {e}")
    
    # Try to register with a simple handler
    print("\nTrying to register handler...")
    
    # In MCP 2.x, we might need to use a different approach
    # Let's try to add a request handler for "tools/call"
    
    # First, let's check if there are any existing handlers
    print(f"Existing request handlers: {app._request_handlers}")
    
    # Try to add a handler
    # The handler might need to be a coroutine function
    
    async def test_handler(params):
        """Test handler."""
        return {"result": "test"}
    
    # Try to register
    app.add_request_handler("tools/call", test_handler)
    print("✅ Handler registered")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()


async def main():
    """Test MCP server."""
    print("\n🚀 Testing MCP server...")
    
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            print("✅ stdio server created")
            
            # Try to run
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
            
    except Exception as e:
        print(f"❌ Error running server: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())