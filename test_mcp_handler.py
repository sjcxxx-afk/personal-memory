#!/usr/bin/env python3
"""
Test MCP server with request handler.
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
# Note: MCP 2.x uses a different API
# We need to check the correct method name

async def main():
    """Test MCP server with handler."""
    print("🚀 Testing MCP server with handler...")
    
    # Check available methods for registering handlers
    print("Available methods for registering handlers:")
    for method in dir(app):
        if 'handler' in method.lower() or 'register' in method.lower():
            print(f"   - {method}")
    
    # Try to register the handler
    try:
        # In MCP 2.x, we might need to use add_request_handler
        # The method signature might be different
        
        # Let's check the source code
        import inspect
        from mcp.server.lowlevel.server import Server as LowLevelServer
        
        # Get the add_request_handler method
        if hasattr(LowLevelServer, 'add_request_handler'):
            method = getattr(LowLevelServer, 'add_request_handler')
            sig = inspect.signature(method)
            print(f"\nadd_request_handler signature: {sig}")
            
            # Try to understand the parameters
            print("Parameters:")
            for param_name, param in sig.parameters.items():
                print(f"   {param_name}: {param.annotation}")
        
        # Try to register the handler
        # The method might expect a specific handler type
        
        print("\nTrying to register handler...")
        
        # In MCP 2.x, we might need to use a different approach
        # Let's check if there are any examples
        
        # For now, let's try to run the server without registering handlers
        print("Running server without handlers...")
        
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            print("✅ stdio server created")
            
            # Try to run
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())