#!/usr/bin/env python3
"""
Basic test for Personal Memory Service
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.models import Fact, MemoryPoint, SearchResult
        print("✅ Models imported successfully")
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return False
    
    try:
        from src.storage.fact_store import FactStore
        print("✅ FactStore imported successfully")
    except Exception as e:
        print(f"❌ Error importing FactStore: {e}")
        return False
    
    try:
        from src.storage.vector_store import VectorStore
        print("✅ VectorStore imported successfully")
    except Exception as e:
        print(f"❌ Error importing VectorStore: {e}")
        return False
    
    try:
        from src.tools.store_tool import StoreTool
        print("✅ StoreTool imported successfully")
    except Exception as e:
        print(f"❌ Error importing StoreTool: {e}")
        return False
    
    try:
        from src.tools.search_tool import SearchTool
        print("✅ SearchTool imported successfully")
    except Exception as e:
        print(f"❌ Error importing SearchTool: {e}")
        return False
    
    return True


def test_fact_store():
    """Test FactStore functionality."""
    print("\nTesting FactStore...")
    
    try:
        from src.storage.fact_store import FactStore
        from src.models import Fact
        from datetime import datetime
        
        # Create store
        store = FactStore()
        print("✅ FactStore created")
        
        # Create a fact
        fact = Fact(
            content="Test fact content",
            scene="test",
            timestamp=datetime.now(),
            source="test",
            importance="medium"
        )
        print(f"✅ Fact created: {fact.id}")
        
        # Store fact
        success = store.store_fact(fact)
        print(f"✅ Fact stored: {success}")
        
        # Retrieve fact
        retrieved = store.get_fact(fact.id)
        print(f"✅ Fact retrieved: {retrieved is not None}")
        
        # List facts
        facts = store.get_all_facts(limit=10)
        print(f"✅ Facts listed: {len(facts)} facts found")
        
        return True
    except Exception as e:
        print(f"❌ FactStore test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vector_store():
    """Test VectorStore functionality."""
    print("\nTesting VectorStore...")
    
    try:
        from src.storage.vector_store import VectorStore
        
        # Create store
        store = VectorStore()
        print("✅ VectorStore created")
        
        # Add fact
        success = store.add_fact(
            fact_id="test-123",
            content="This is a test fact about Python programming",
            metadata={"scene": "work", "source": "test"}
        )
        print(f"✅ Fact added to vector store: {success}")
        
        # Search facts
        results = store.search_facts(query="Python programming", n_results=3)
        print(f"✅ Search results: {len(results)} found")
        
        # Get stats
        stats = store.get_collection_stats()
        print(f"✅ Collection stats: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ VectorStore test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tools():
    """Test MCP tools."""
    print("\nTesting MCP tools...")
    
    try:
        import asyncio
        from src.tools.store_tool import StoreTool
        from src.tools.search_tool import SearchTool
        
        # Create tools
        store_tool = StoreTool()
        search_tool = SearchTool()
        print("✅ MCP tools created")
        
        # Test store tool
        async def test_store():
            result = await store_tool.store_fact(
                content="Test fact from MCP tool",
                scene="test",
                source="test",
                importance="medium"
            )
            return result
        
        result = asyncio.run(test_store())
        print(f"✅ Store tool result: {result[0].text[:50]}...")
        
        # Test search tool
        async def test_search():
            result = await search_tool.search_facts(
                query="MCP tool",
                limit=3
            )
            return result
        
        result = asyncio.run(test_search())
        print(f"✅ Search tool result: {result[0].text[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🧪 Personal Memory Service - Basic Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_fact_store,
        test_vector_store,
        test_tools
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
        print("\n🎉 All tests passed! The basic functionality is working.")
        print("\n💡 You can now start the MCP server with:")
        print("   python -m src.server")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())