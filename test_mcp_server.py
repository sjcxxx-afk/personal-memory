#!/usr/bin/env python3
"""
Test MCP server with a simple tool.
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


# Define a simple tool
async def test_tool(query: str) -> list[TextContent]:
    """A simple test tool."""
    return [TextContent(
        type="text",
        text=f"✅ Test tool called with query: {query}"
    )]


# Register the tool
# Note: MCP 2.x uses a different API
# We need to check the correct way to register tools

async def main():
    """Test MCP server."""
    print("🚀 Testing MCP server...")
    
    # Check if we can add tools
    print(f"Server type: {type(app)}")
    print(f"Server attributes: {[attr for attr in dir(app) if not attr.startswith('_')]}")
    
    # Try to run the server
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