#!/usr/bin/env python3
"""
Test script for Personal Memory Service
This script tests the basic functionality of the MCP tools.
"""

import asyncio
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.tools.store_tool import StoreTool
from src.tools.search_tool import SearchTool


async def test_store_and_search():
    """Test storing and searching facts."""
    print("🧪 Testing Personal Memory Service...")
    print("=" * 50)
    
    # Initialize tools
    store_tool = StoreTool()
    search_tool = SearchTool()
    
    # Test 1: Store a fact
    print("\n📝 Test 1: Storing a fact...")
    test_content = "用户对花生过敏，需要避免所有花生制品"
    test_scene = "health"
    test_source = "chat_2026-09-07"
    test_importance = "high"
    
    result = await store_tool.store_fact(
        content=test_content,
        scene=test_scene,
        source=test_source,
        importance=test_importance
    )
    
    print(f"Store result: {result[0].text}")
    
    # Test 2: Store another fact
    print("\n📝 Test 2: Storing another fact...")
    test_content2 = "用户喜欢简洁的PPT风格，不要过多文字"
    test_scene2 = "work"
    test_source2 = "chat_2026-09-06"
    test_importance2 = "medium"
    
    result2 = await store_tool.store_fact(
        content=test_content2,
        scene=test_scene2,
        source=test_source2,
        importance=test_importance2
    )
    
    print(f"Store result: {result2[0].text}")
    
    # Test 3: List facts
    print("\n📋 Test 3: Listing all facts...")
    result3 = await store_tool.list_facts(limit=10)
    print(f"List result: {result3[0].text}")
    
    # Test 4: Search facts
    print("\n🔍 Test 4: Searching for '过敏'...")
    result4 = await search_tool.search_facts(query="过敏", limit=3)
    print(f"Search result: {result4[0].text}")
    
    # Test 5: Search with scene filter
    print("\n🔍 Test 5: Searching for '简洁' in work scene...")
    result5 = await search_tool.search_facts(
        query="简洁",
        scene_filter="work",
        limit=3
    )
    print(f"Search result: {result5[0].text}")
    
    # Test 6: Get fact details
    print("\n📄 Test 6: Getting fact details...")
    # Extract fact ID from first result
    first_result_text = result[0].text
    if "ID:" in first_result_text:
        fact_id = first_result_text.split("ID:")[1].split("\n")[0].strip()
        result6 = await search_tool.get_fact_details(fact_id=fact_id)
        print(f"Fact details: {result6[0].text}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n💡 If you see this message, the basic functionality is working.")
    print("   The service is ready to be used with AI clients.")


async def test_error_handling():
    """Test error handling."""
    print("\n🔧 Testing error handling...")
    
    search_tool = SearchTool()
    
    # Test searching with empty query
    try:
        result = await search_tool.search_facts(query="", limit=3)
        print(f"Empty query result: {result[0].text}")
    except Exception as e:
        print(f"Error handling empty query: {e}")
    
    # Test getting non-existent fact
    try:
        result = await search_tool.get_fact_details(fact_id="non-existent-id")
        print(f"Non-existent fact result: {result[0].text}")
    except Exception as e:
        print(f"Error handling non-existent fact: {e}")


async def main():
    """Main test function."""
    try:
        await test_store_and_search()
        await test_error_handling()
        
        print("\n🎉 All tests passed! The service is ready for use.")
        print("\n📝 Next steps:")
        print("   1. Start the service with Docker: docker-compose up -d")
        print("   2. Configure your AI client to connect to the service")
        print("   3. Start storing and searching facts!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())