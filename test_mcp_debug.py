#!/usr/bin/env python3
"""
Debug MCP tool call.
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
    print("🧪 Debug MCP Tool Call...")
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
                    print(f"\n  Tool: {tool.name}")
                    print(f"    Description: {tool.description}")
                    print(f"    Input Schema: {json.dumps(tool.input_schema, indent=6)}")
                
                # Test store_fact tool with detailed error handling
                print("\n📝 Testing store_fact with debug...")
                try:
                    # Try to call the tool
                    result = await session.call_tool(
                        "store_fact",
                        arguments={
                            "content": "测试事实",
                            "scene": "test",
                            "source": "test",
                            "importance": "medium"
                        }
                    )
                    print(f"✅ Result: {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    print(f"   Error type: {type(e)}")
                    
                    # Try to get more details
                    import traceback
                    traceback.print_exc()
                
                # Try with minimal arguments
                print("\n📝 Testing store_fact with minimal arguments...")
                try:
                    result = await session.call_tool(
                        "store_fact",
                        arguments={
                            "content": "测试事实"
                        }
                    )
                    print(f"✅ Result: {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                print("\n" + "=" * 50)
                print("Debug completed!")
                
    except Exception as e:
        print(f"\n❌ Failed to connect to MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Main test function."""
    print("🚀 MCP Debug Test")
    print("=" * 50)
    
    success = await test_mcp_server()
    
    if success:
        print("\n✅ Debug completed!")
        return 0
    else:
        print("\n⚠️  Debug failed.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))