#!/usr/bin/env python3
"""
Detailed MCP server test.
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


# Check MCP version and API
print("MCP Server API Analysis:")
print("=" * 50)

# Check for tool registration methods
print("1. Checking for tool registration methods:")
for method in dir(app):
    if 'tool' in method.lower() or 'register' in method.lower():
        print(f"   - {method}")

print("\n2. Checking for request handler methods:")
for method in dir(app):
    if 'handler' in method.lower() or 'request' in method.lower():
        print(f"   - {method}")

print("\n3. Checking Server class documentation:")
if hasattr(Server, '__doc__'):
    print(f"   Documentation: {Server.__doc__}")

print("\n4. Checking for examples in MCP package:")
try:
    import mcp.server.lowlevel.server as server_module
    print(f"   Module path: {server_module.__file__}")
except Exception as e:
    print(f"   Error: {e}")

print("\n5. Testing tool creation:")
try:
    # Create a tool
    tool = Tool(
        name="test_tool",
        description="A test tool",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            }
        }
    )
    print(f"   ✅ Tool created: {tool.name}")
except Exception as e:
    print(f"   ❌ Error creating tool: {e}")

print("\n6. Checking for tool registration examples:")
# Try to find examples in the MCP package
try:
    import inspect
    from mcp.server.lowlevel.server import Server as LowLevelServer
    
    # Check if there's a register_tool method
    for name, method in inspect.getmembers(LowLevelServer):
        if 'tool' in name.lower():
            print(f"   Found method: {name}")
            # Get method signature
            try:
                sig = inspect.signature(method)
                print(f"     Signature: {sig}")
            except:
                pass
except Exception as e:
    print(f"   Error: {e}")

print("\n7. Testing add_request_handler:")
try:
    # Check if we can add a request handler
    print(f"   add_request_handler method exists: {hasattr(app, 'add_request_handler')}")
    
    if hasattr(app, 'add_request_handler'):
        # Try to add a handler
        async def test_handler(params):
            return {"result": "test"}
        
        # This might not be the correct way
        print("   Note: add_request_handler exists but usage may vary")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 50)
print("Analysis complete.")