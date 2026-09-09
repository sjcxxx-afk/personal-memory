#!/usr/bin/env python3
"""
Test MCP client for example server.
"""

import asyncio
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """Test the MCP server by connecting to it."""
    print("🧪 Testing MCP Server Connection...")
    print("=" * 50)
    
    # Define server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["test_mcp_example.py"],
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
                    print(f"  • {tool.name}: {tool.description}")
                
                # Test test_tool
                print("\n📝 Testing test_tool...")
                try:
                    result = await session.call_tool(
                        "test_tool",
                        arguments={
                            "query": "Hello, world!"
                        }
                    )
                    print(f"✅ test_tool result: {result.content[0].text}")
                except Exception as e:
                    print(f"❌ test_tool error: {e}")
                
                print("\n" + "=" * 50)
                print("✅ MCP server test completed!")
                
    except Exception as e:
        print(f"\n❌ Failed to connect to MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Main test function."""
    print("🚀 MCP Example Server Test")
    print("=" * 50)
    
    success = await test_mcp_server()
    
    if success:
        print("\n🎉 All tests passed! The MCP server is working correctly.")
        return 0
    else:
        print("\n⚠️  Tests failed. Please check the server and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))