#!/usr/bin/env python3
"""
Raw MCP tool call test.
"""

import asyncio
import sys
import os
import json

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """Test the MCP server by connecting to it."""
    print("🧪 Raw MCP Tool Call Test...")
    print("=" * 50)
    
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.server"],
        env={"PYTHONPATH": project_root}
    )
    
    try:
        # Connect to the server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ Connected to MCP server")
                
                # List available tools
                print("\n📋 Listing available tools...")
                tools = await session.list_tools()
                print(f"Found {len(tools.tools)} tools:")
                
                for tool in tools.tools:
                    print(f"  • {tool.name}")
                
                # Try to call a tool using send_request
                print("\n📝 Testing raw tool call...")
                
                # Prepare the request
                request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "store_fact",
                        "arguments": {
                            "content": "测试事实",
                            "scene": "test",
                            "source": "test",
                            "importance": "medium"
                        }
                    }
                }
                
                print(f"Request: {json.dumps(request, indent=2)}")
                
                # Send the request
                try:
                    # Use the session's send_request method
                    result = await session.send_request(
                        method="tools/call",
                        params={
                            "name": "store_fact",
                            "arguments": {
                                "content": "测试事实",
                                "scene": "test",
                                "source": "test",
                                "importance": "medium"
                            }
                        }
                    )
                    print(f"✅ Success: {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    print(f"   Error type: {type(e)}")
                    
                    # Try to get more details
                    import traceback
                    traceback.print_exc()
                
                print("\n" + "=" * 50)
                print("Test completed!")
                
    except Exception as e:
        print(f"\n❌ Failed to connect to MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Main test function."""
    print("🚀 Raw MCP Tool Call Test")
    print("=" * 50)
    
    success = await test_mcp_server()
    
    if success:
        print("\n✅ Test completed!")
        return 0
    else:
        print("\n⚠️  Test failed.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))