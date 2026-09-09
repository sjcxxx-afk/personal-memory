#!/usr/bin/env python3
"""
Final MCP client test for Personal Memory Service.
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
    print("🧪 Testing Personal Memory MCP Server...")
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
                    print(f"  • {tool.name}: {tool.description[:50]}...")
                
                # Test store_fact tool
                print("\n📝 Test 1: store_fact")
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
                    print(f"✅ Result: {result.content[0].text[:100]}...")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test store_fact again
                print("\n📝 Test 2: store_fact (another)")
                try:
                    result = await session.call_tool(
                        "store_fact",
                        arguments={
                            "content": "用户喜欢简洁的PPT风格，不要太多文字",
                            "scene": "work",
                            "source": "test",
                            "importance": "medium"
                        }
                    )
                    print(f"✅ Result: {result.content[0].text[:100]}...")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test list_facts tool
                print("\n📋 Test 3: list_facts")
                try:
                    result = await session.call_tool(
                        "list_facts",
                        arguments={
                            "limit": 10
                        }
                    )
                    print(f"✅ Result: {result.content[0].text[:150]}...")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test search_facts tool
                print("\n🔍 Test 4: search_facts")
                try:
                    result = await session.call_tool(
                        "search_facts",
                        arguments={
                            "query": "过敏",
                            "limit": 5
                        }
                    )
                    print(f"✅ Result: {result.content[0].text[:150]}...")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test get_memory_stats tool
                print("\n📊 Test 5: get_memory_stats")
                try:
                    result = await session.call_tool(
                        "get_memory_stats",
                        arguments={}
                    )
                    print(f"✅ Result: {result.content[0].text[:150]}...")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                print("\n" + "=" * 50)
                print("✅ All MCP tests completed!")
                
    except Exception as e:
        print(f"\n❌ Failed to connect to MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


async def main():
    """Main test function."""
    print("🚀 Personal Memory Service - Final MCP Test")
    print("=" * 50)
    
    success = await test_mcp_server()
    
    if success:
        print("\n🎉 All tests passed! The MCP server is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Configure Claude Desktop with the provided config")
        print("   2. Start using the memory service with your AI")
        return 0
    else:
        print("\n⚠️  Tests failed. Please check the server and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))