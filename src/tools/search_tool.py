from typing import List, Optional
from datetime import datetime
from mcp.types import TextContent

from ..models import Fact, SearchResult
from ..storage.fact_store import FactStore
from ..storage.vector_store import VectorStore


class SearchTool:
    """MCP tool for searching facts."""
    
    def __init__(self):
        self.fact_store = FactStore()
        self.vector_store = VectorStore()
    
    async def search_facts(self, query: str, scene_filter: str = None, 
                          limit: int = 5) -> List[TextContent]:
        """
        Search for facts using semantic similarity.
        
        Args:
            query: Search query
            scene_filter: Optional scene tag to filter by
            limit: Maximum number of results to return
        
        Returns:
            List of TextContent with search results
        """
        try:
            # First try vector search
            vector_results = []
            try:
                # Prepare ChromaDB filter
                where_filter = None
                if scene_filter:
                    where_filter = {"scene": scene_filter}
                
                # Search in vector store
                vector_results = self.vector_store.search_facts(
                    query=query,
                    n_results=limit,
                    where=where_filter
                )
            except Exception as e:
                print(f"Vector search failed, falling back to SQLite: {e}")
            
            # If vector search returns results, use them
            if vector_results:
                # Get full fact details from SQLite
                search_results = []
                for result in vector_results:
                    fact = self.fact_store.get_fact(result["id"])
                    if fact:
                        # Update access count
                        self.fact_store.update_access(fact.id)
                        
                        # Calculate relevance score (inverse of distance)
                        # ChromaDB returns distances, lower is better
                        # Convert to similarity score (0-1)
                        distance = result.get("distance", 0.0)
                        similarity = max(0.0, 1.0 - distance)  # Simple conversion
                        
                        search_results.append(SearchResult(
                            fact=fact,
                            score=similarity
                        ))
                
                if search_results:
                    # Sort by similarity score (highest first)
                    search_results.sort(key=lambda x: x.score, reverse=True)
                    
                    # Format results
                    result_lines = []
                    for i, result in enumerate(search_results, 1):
                        fact = result.fact
                        result_lines.append(
                            f"{i}. [{fact.scene}] {fact.content}\n"
                            f"   Similarity: {result.score:.2f}\n"
                            f"   ID: {fact.id}\n"
                            f"   Source: {fact.source} | Importance: {fact.importance}\n"
                            f"   Temperature: {fact.temperature} | Accessed: {fact.access_count} times"
                        )
                    
                    header = f"🔍 Found {len(search_results)} fact(s) matching: '{query}'"
                    if scene_filter:
                        header += f" in scene '{scene_filter}'"
                    
                    return [TextContent(
                        type="text",
                        text=f"{header}:\n\n" + "\n\n".join(result_lines)
                    )]
            
            # Fallback to SQLite search
            print(f"Falling back to SQLite search for: {query}")
            
            # Search using SQLite LIKE query
            conn = self.fact_store._get_connection()
            cursor = conn.cursor()
            
            try:
                if scene_filter:
                    cursor.execute('''
                        SELECT * FROM facts 
                        WHERE content LIKE ? AND scene = ?
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    ''', (f'%{query}%', scene_filter, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM facts 
                        WHERE content LIKE ? 
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    ''', (f'%{query}%', limit))
                
                rows = cursor.fetchall()
                
                if not rows:
                    return [TextContent(
                        type="text",
                        text=f"🔍 No facts found matching: '{query}'"
                    )]
                
                # Convert to Fact objects
                search_results = []
                for row in rows:
                    fact = Fact(
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
                    
                    # Update access count
                    self.fact_store.update_access(fact.id)
                    
                    # SQLite search gets a default score of 0.8
                    search_results.append(SearchResult(
                        fact=fact,
                        score=0.8
                    ))
                
                # Format results
                result_lines = []
                for i, result in enumerate(search_results, 1):
                    fact = result.fact
                    result_lines.append(
                        f"{i}. [{fact.scene}] {fact.content}\n"
                        f"   ID: {fact.id}\n"
                        f"   Source: {fact.source} | Importance: {fact.importance}\n"
                        f"   Temperature: {fact.temperature} | Accessed: {fact.access_count} times"
                    )
                
                header = f"🔍 Found {len(search_results)} fact(s) matching: '{query}'"
                if scene_filter:
                    header += f" in scene '{scene_filter}'"
                
                return [TextContent(
                    type="text",
                    text=f"{header}:\n\n" + "\n\n".join(result_lines)
                )]
                
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Error searching facts: {str(e)}\n\n"
                         f"Query: {query}"
                )]
            finally:
                conn.close()
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error searching facts: {str(e)}\n\n"
                     f"Query: {query}"
            )]
    
    async def get_fact_details(self, fact_id: str) -> List[TextContent]:
        """
        Get detailed information about a specific fact.
        
        Args:
            fact_id: ID of the fact to retrieve
        
        Returns:
            List of TextContent with fact details
        """
        try:
            fact = self.fact_store.get_fact(fact_id)
            
            if not fact:
                return [TextContent(
                    type="text",
                    text=f"❌ Fact not found with ID: {fact_id}"
                )]
            
            # Update access count
            self.fact_store.update_access(fact.id)
            
            # Format detailed information
            details = [
                f"📄 Fact Details:",
                f"",
                f"ID: {fact.id}",
                f"Content: {fact.content}",
                f"Scene: {fact.scene}",
                f"Source: {fact.source}",
                f"Importance: {fact.importance}",
                f"Temperature: {fact.temperature}",
                f"Access Count: {fact.access_count}",
                f"Last Accessed: {fact.last_accessed.isoformat() if fact.last_accessed else 'Never'}",
                f"Created: {fact.timestamp.isoformat()}"
            ]
            
            return [TextContent(
                type="text",
                text="\n".join(details)
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error getting fact details: {str(e)}\n\n"
                     f"Fact ID: {fact_id}"
            )]