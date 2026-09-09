#!/usr/bin/env python3
"""
Test MCP server creation.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_mcp_import():
    """Test MCP imports."""
    print("Testing MCP imports...")
    
    try:
        from mcp.server import Server
        print("✅ Server imported")
    except Exception as e:
        print(f"❌ Error importing Server: {e}")
        return False
    
    try:
        from mcp.types import Tool, TextContent
        print("✅ Tool and TextContent imported")
    except Exception as e:
        print(f"❌ Error importing Tool/TextContent: {e}")
        return False
    
    try:
        import mcp.server.stdio
        print("✅ mcp.server.stdio imported")
    except Exception as e:
        print(f"❌ Error importing mcp.server.stdio: {e}")
        return False
    
    return True


def test_server_creation():
    """Test server creation."""
    print("\nTesting server creation...")
    
    try:
        from mcp.server import Server
        
        # Create server
        app = Server("test-server")
        print(f"✅ Server created: {app}")
        
        # Check available methods
        print(f"   Available methods: {[m for m in dir(app) if not m.startswith('_')]}")
        
        # Check if tool decorator exists
        if hasattr(app, 'tool'):
            print("   ✅ app.tool() method exists")
        else:
            print("   ❌ app.tool() method does not exist")
            
            # Check for alternative methods
            for method in dir(app):
                if 'tool' in method.lower():
                    print(f"   Found tool-related method: {method}")
        
        return True
    except Exception as e:
        print(f"❌ Server creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mcp_types():
    """Test MCP types."""
    print("\nTesting MCP types...")
    
    try:
        from mcp.types import Tool, TextContent
        
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
        print(f"✅ Tool created: {tool.name}")
        
        # Create text content
        content = TextContent(type="text", text="Hello, world!")
        print(f"✅ TextContent created: {content.text}")
        
        return True
    except Exception as e:
        print(f"❌ MCP types test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🧪 MCP Server Test")
    print("=" * 50)
    
    tests = [
        test_mcp_import,
        test_server_creation,
        test_mcp_types
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 All MCP tests passed!")
        return 0
    else:
        print("\n⚠️  Some MCP tests failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())