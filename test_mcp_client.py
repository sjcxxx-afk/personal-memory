#!/usr/bin/env python3
"""
Test MCP client to verify the server works correctly.
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
        args=["run_server.py"],
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
                
                # Test store_fact tool
                print("\n📝 Testing store_fact tool...")
                try:
                    result = await session.call_tool(
                        "store_fact",
                        arguments={
                            "content": "用户对花生过敏，需要避免所有花生制品",
                            "scene": "health",
                            "source": "test",
                            "importance": "high"
                        }
                    )
                    print(f"✅ store_fact result: {result.content[0].text[:100]}...")
                except Exception as e:
                    print(f"❌ store_fact error: {e}")
                
                # Test search_facts tool
                print("\n🔍 Testing search_facts tool...")
                try:
                    result = await session.call_tool(
                        "search_facts",
                        arguments={
                            "query": "过敏",
                            "limit": 3
                        }
                    )
                    print(f"✅ search_facts result: {result.content[0].text[:100]}...")
                except Exception as e:
                    print(f"❌ search_facts error: {e}")
                
                # Test list_facts tool
                print("\n📋 Testing list_facts tool...")
                try:
                    result = await session.call_tool(
                        "list_facts",
                        arguments={
                            "limit": 5
                        }
                    )
                    print(f"✅ list_facts result: {result.content[0].text[:100]}...")
                except Exception as e:
                    print(f"❌ list_facts error: {e}")
                
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
    print("🚀 Personal Memory Service - MCP Client Test")
    print("=" * 50)
    
    success = await test_mcp_server()
    
    if success:
        print("\n🎉 All tests passed! The MCP server is working correctly.")
        print("\n💡 You can now configure your AI client to use this server.")
        return 0
    else:
        print("\n⚠️  Tests failed. Please check the server and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))