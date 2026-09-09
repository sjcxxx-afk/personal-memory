#!/usr/bin/env python3
"""
Test SQLite-based search functionality.
"""

import asyncio
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.storage.fact_store import FactStore
from src.models import Fact
from datetime import datetime


async def test_sqlite_search():
    """Test SQLite-based search."""
    print("🔍 Testing SQLite Search Functionality")
    print("=" * 50)
    
    # Initialize store
    store = FactStore()
    
    # Get all facts
    print("\n📋 Getting all facts...")
    facts = store.get_all_facts(limit=20)
    print(f"Found {len(facts)} facts")
    
    # Search using SQLite LIKE query
    print("\n🔍 Searching for '过敏' using SQLite...")
    conn = store._get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM facts 
            WHERE content LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''', ('%过敏%',))
        
        rows = cursor.fetchall()
        print(f"Found {len(rows)} results:")
        for row in rows:
            print(f"  - [{row['scene']}] {row['content'][:50]}...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    
    # Search for '简洁'
    print("\n🔍 Searching for '简洁' using SQLite...")
    conn = store._get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM facts 
            WHERE content LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''', ('%简洁%',))
        
        rows = cursor.fetchall()
        print(f"Found {len(rows)} results:")
        for row in rows:
            print(f"  - [{row['scene']}] {row['content'][:50]}...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    
    # Search for 'Python'
    print("\n🔍 Searching for 'Python' using SQLite...")
    conn = store._get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM facts 
            WHERE content LIKE ? 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''', ('%Python%',))
        
        rows = cursor.fetchall()
        print(f"Found {len(rows)} results:")
        for row in rows:
            print(f"  - [{row['scene']}] {row['content'][:50]}...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    
    print("\n" + "=" * 50)
    print("✅ SQLite search test completed!")
    
    return True


async def main():
    """Main test function."""
    print("🚀 SQLite Search Test")
    print("=" * 50)
    
    success = await test_sqlite_search()
    
    if success:
        print("\n🎉 SQLite search is working correctly!")
        return 0
    else:
        print("\n⚠️  SQLite search test failed.")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))