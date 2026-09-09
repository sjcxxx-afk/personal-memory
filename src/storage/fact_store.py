import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..models import Fact
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import SQLITE_DB_PATH

# Set up logger
logger = logging.getLogger(__name__)


class FactStore:
    """SQLite-based storage for fact metadata."""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or SQLITE_DB_PATH
        self._init_db()
    
    def _init_db(self):
        """Initialize database with schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create facts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                scene TEXT DEFAULT 'general',
                timestamp TEXT NOT NULL,
                source TEXT DEFAULT 'chat',
                importance TEXT DEFAULT 'medium',
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                temperature TEXT DEFAULT 'hot'
            )
        ''')
        
        # Create index on scene and timestamp
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_facts_scene ON facts(scene)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_facts_timestamp ON facts(timestamp)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_facts_temperature ON facts(temperature)
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def store_fact(self, fact: Fact) -> bool:
        """Store a fact in the database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO facts 
                (id, content, scene, timestamp, source, importance, 
                 access_count, last_accessed, temperature)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                fact.id,
                fact.content,
                fact.scene,
                fact.timestamp.isoformat(),
                fact.source,
                fact.importance,
                fact.access_count,
                fact.last_accessed.isoformat() if fact.last_accessed else None,
                fact.temperature
            ))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error storing fact: {e}")
            return False
        finally:
            conn.close()
    
    def get_fact(self, fact_id: str) -> Optional[Fact]:
        """Retrieve a fact by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM facts WHERE id = ?', (fact_id,))
            row = cursor.fetchone()
            
            if row:
                return Fact(
                    id=row['id'],
                    content=row['content'],
                    scene=row['scene'],
                    timestamp=datetime.fromisoformat(row['timestamp']),
                    source=row['source'],
                    importance=row['importance'],
                    access_count=row['access_count'],
                    last_accessed=datetime.fromisoformat(row['last_accessed']) if row['last_accessed'] else None,
                    temperature=row['temperature']
                )
            return None
        except Exception as e:
            logger.error(f"Error getting fact: {e}")
            return None
        finally:
            conn.close()
    
    def update_access(self, fact_id: str) -> bool:
        """Update access count and last_accessed time."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE facts 
                SET access_count = access_count + 1,
                    last_accessed = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), fact_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating access: {e}")
            return False
        finally:
            conn.close()
    
    def get_facts_by_scene(self, scene: str, limit: int = 10) -> List[Fact]:
        """Get facts by scene tag."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM facts 
                WHERE scene = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (scene, limit))
            
            rows = cursor.fetchall()
            return [Fact(
                id=row['id'],
                content=row['content'],
                scene=row['scene'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                source=row['source'],
                importance=row['importance'],
                access_count=row['access_count'],
                last_accessed=datetime.fromisoformat(row['last_accessed']) if row['last_accessed'] else None,
                temperature=row['temperature']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting facts by scene: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_facts(self, limit: int = 100, offset: int = 0) -> List[Fact]:
        """Get all facts with pagination."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM facts 
                ORDER BY timestamp DESC 
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            rows = cursor.fetchall()
            return [Fact(
                id=row['id'],
                content=row['content'],
                scene=row['scene'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                source=row['source'],
                importance=row['importance'],
                access_count=row['access_count'],
                last_accessed=datetime.fromisoformat(row['last_accessed']) if row['last_accessed'] else None,
                temperature=row['temperature']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting all facts: {e}")
            return []
        finally:
            conn.close()
    
    def delete_fact(self, fact_id: str) -> bool:
        """Delete a fact by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM facts WHERE id = ?', (fact_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting fact: {e}")
            return False
        finally:
            conn.close()
    
    def update_temperature(self, fact_id: str, temperature: str) -> bool:
        """Update fact temperature."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE facts 
                SET temperature = ?
                WHERE id = ?
            ''', (temperature, fact_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating temperature: {e}")
            return False
        finally:
            conn.close()
    
    def get_facts_by_temperature(self, temperature: str, limit: int = 100) -> List[Fact]:
        """Get facts by temperature status."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM facts 
                WHERE temperature = ? 
                ORDER BY last_accessed DESC NULLS LAST
                LIMIT ?
            ''', (temperature, limit))
            
            rows = cursor.fetchall()
            return [Fact(
                id=row['id'],
                content=row['content'],
                scene=row['scene'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                source=row['source'],
                importance=row['importance'],
                access_count=row['access_count'],
                last_accessed=datetime.fromisoformat(row['last_accessed']) if row['last_accessed'] else None,
                temperature=row['temperature']
            ) for row in rows]
        except Exception as e:
            print(f"Error getting facts by temperature: {e}")
            return []
        finally:
            conn.close()