#!/usr/bin/env python3
"""
Debug search functionality.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.storage.vector_store_simple import SimpleVectorStore


def test_search():
    """Test search functionality."""
    print("🔍 Debug Search Functionality")
    print("=" * 50)
    
    # Create store
    store = SimpleVectorStore("test")
    
    # Add some facts
    facts = [
        ("fact1", "用户对花生过敏，需要避免所有花生制品", {"scene": "health"}),
        ("fact2", "用户喜欢简洁的PPT风格，不要太多文字", {"scene": "work"}),
        ("fact3", "用户每天早上7点起床，晚上11点睡觉", {"scene": "life"}),
        ("fact4", "用户正在学习Python编程，目标是掌握数据分析", {"scene": "education"}),
    ]
    
    for fact_id, content, metadata in facts:
        store.add_fact(fact_id, content, metadata)
        print(f"Added: {fact_id} - {content[:20]}...")
    
    # Test tokenization
    print("\n📝 Tokenization test:")
    test_texts = ["过敏", "花生过敏", "用户对花生过敏"]
    for text in test_texts:
        tokens = store._tokenize(text)
        print(f"  '{text}' -> {tokens}")
    
    # Check inverted index
    print("\n📋 Inverted index:")
    for token, fact_ids in store.inverted_index.items():
        if len(token) == 1 and ord(token) > 127:  # Chinese characters
            print(f"  '{token}': {fact_ids}")
    
    # Test search
    print("\n🔍 Search tests:")
    queries = ["过敏", "花生", "简洁", "Python"]
    for query in queries:
        results = store.search_facts(query, n_results=3)
        print(f"\n  Query: '{query}'")
        print(f"  Results: {len(results)}")
        for result in results:
            print(f"    - {result['id']}: {result['content'][:30]}...")
    
    print("\n" + "=" * 50)
    print("Debug completed!")


if __name__ == "__main__":
    test_search()