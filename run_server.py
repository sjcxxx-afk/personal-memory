#!/usr/bin/env python3
"""
Run the Personal Memory MCP Server.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """Run the MCP server."""
    import sys
    print("🚀 Personal Memory MCP Server", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    try:
        # Import and run the server
        from src.server import main as server_main
        import asyncio
        
        print("✅ Server modules loaded successfully", file=sys.stderr)
        print("🔌 Starting MCP server on stdio...", file=sys.stderr)
        print("   Connect using MCP client like Claude Desktop", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        # Run the server
        asyncio.run(server_main())
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"\n❌ Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())