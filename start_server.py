#!/usr/bin/env python3
"""
Start the Personal Memory MCP Server.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """Start the MCP server."""
    print("🚀 Starting Personal Memory MCP Server...")
    print("=" * 50)
    
    try:
        # Import and run the server
        from src.server import main as server_main
        import asyncio
        
        print("✅ Server modules loaded successfully")
        print("🔌 Starting MCP server on stdio...")
        print("   (Connect using MCP client like Claude Desktop)")
        print("=" * 50)
        
        # Run the server
        asyncio.run(server_main())
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())