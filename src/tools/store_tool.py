from typing import List
from mcp.types import TextContent
from datetime import datetime

from ..models import Fact
from ..storage.fact_store import FactStore
from ..storage.vector_store import VectorStore


class StoreTool:
    """MCP tool for storing facts."""
    
    def __init__(self):
        self.fact_store = FactStore()
        self.vector_store = VectorStore()
    
    async def store_fact(self, content: str, scene: str = "general", 
                        source: str = "chat", importance: str = "medium") -> List[TextContent]:
        """
        Store a fact in the memory service.
        
        Args:
            content: The factual content to store
            scene: Scene tag (work, life, health, etc.)
            source: Source of the fact (chat_2026-09-07, note, etc.)
            importance: Importance level (high, medium, low)
        
        Returns:
            List of TextContent with storage result
        """
        try:
            # Create Fact object
            fact = Fact(
                content=content,
                scene=scene,
                timestamp=datetime.now(),
                source=source,
                importance=importance
            )
            
            # Store in SQLite (metadata)
            sqlite_success = self.fact_store.store_fact(fact)
            
            # Store in ChromaDB (vector)
            vector_metadata = {
                "scene": scene,
                "source": source,
                "importance": importance,
                "timestamp": fact.timestamp.isoformat()
            }
            vector_success = self.vector_store.add_fact(
                fact_id=fact.id,
                content=content,
                metadata=vector_metadata
            )
            
            if sqlite_success and vector_success:
                return [TextContent(
                    type="text",
                    text=f"✅ Fact stored successfully!\n\n"
                         f"ID: {fact.id}\n"
                         f"Content: {content}\n"
                         f"Scene: {scene}\n"
                         f"Source: {source}\n"
                         f"Importance: {importance}\n"
                         f"Timestamp: {fact.timestamp.isoformat()}"
                )]
            else:
                error_msg = []
                if not sqlite_success:
                    error_msg.append("Failed to store in SQLite")
                if not vector_success:
                    error_msg.append("Failed to store in ChromaDB")
                
                return [TextContent(
                    type="text",
                    text=f"❌ Partial failure storing fact:\n\n"
                         f"Content: {content}\n"
                         f"Errors: {', '.join(error_msg)}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error storing fact: {str(e)}\n\n"
                     f"Content: {content}"
            )]
    
    async def list_facts(self, scene_filter: str = None, 
                        limit: int = 10) -> List[TextContent]:
        """
        List stored facts.
        
        Args:
            scene_filter: Optional scene tag to filter by
            limit: Maximum number of facts to return
        
        Returns:
            List of TextContent with facts
        """
        try:
            if scene_filter:
                facts = self.fact_store.get_facts_by_scene(scene_filter, limit)
            else:
                facts = self.fact_store.get_all_facts(limit)
            
            if not facts:
                return [TextContent(
                    type="text",
                    text="📭 No facts found."
                )]
            
            # Format facts
            fact_lines = []
            for i, fact in enumerate(facts, 1):
                fact_lines.append(
                    f"{i}. [{fact.scene}] {fact.content}\n"
                    f"   ID: {fact.id}\n"
                    f"   Source: {fact.source} | Importance: {fact.importance}\n"
                    f"   Temperature: {fact.temperature} | Accessed: {fact.access_count} times\n"
                    f"   Stored: {fact.timestamp.strftime('%Y-%m-%d %H:%M')}"
                )
            
            header = f"📋 Found {len(facts)} fact(s)"
            if scene_filter:
                header += f" in scene '{scene_filter}'"
            
            return [TextContent(
                type="text",
                text=f"{header}:\n\n" + "\n\n".join(fact_lines)
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error listing facts: {str(e)}"
            )]