#!/usr/bin/env python3
"""
Simple MCP tool call test.
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
    print("🧪 Simple MCP Tool Call Test...")
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
                
                # Try to call a tool with different parameter formats
                print("\n📝 Testing different parameter formats...")
                
                # Format 1: Direct arguments
                print("\n  Format 1: Direct arguments")
                try:
                    result = await session.call_tool(
                        "store_fact",
                        arguments={"content": "测试事实"}
                    )
                    print(f"  ✅ Success: {result}")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                
                # Format 2: No arguments
                print("\n  Format 2: No arguments")
                try:
                    result = await session.call_tool("get_memory_stats")
                    print(f"  ✅ Success: {result}")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                
                # Format 3: Empty arguments
                print("\n  Format 3: Empty arguments")
                try:
                    result = await session.call_tool(
                        "get_memory_stats",
                        arguments={}
                    )
                    print(f"  ✅ Success: {result}")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                
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
    print("🚀 Simple MCP Tool Call Test")
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