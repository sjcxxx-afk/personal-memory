"""
Vector store implementation.
Currently uses a simple in-memory store for testing.
Can be replaced with ChromaDB or other vector databases.
"""

import logging
from typing import List, Optional, Dict, Any

# Set up logger
logger = logging.getLogger(__name__)

# Try to import ChromaDB, fall back to simple implementation
try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import CHROMA_DB_PATH, EMBEDDING_MODEL, USE_LOCAL_EMBEDDINGS
from .vector_store_simple import SimpleVectorStore


class VectorStore:
    """Vector storage for semantic search."""
    
    def __init__(self, collection_name: str = "facts"):
        self.collection_name = collection_name
        
        # Use ChromaDB if available, otherwise use simple implementation
        if HAS_CHROMADB:
            self._init_chromadb()
        else:
            logger.info("ChromaDB not available, using simple in-memory store")
            self.store = SimpleVectorStore(collection_name)
            self.use_chromadb = False
    
    def _init_chromadb(self):
        """Initialize ChromaDB client and collection."""
        try:
            # Create persistent client
            self.client = chromadb.PersistentClient(
                path=str(CHROMA_DB_PATH),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}  # Use cosine similarity
            )
            
            self.use_chromadb = True
            logger.info(f"ChromaDB collection '{self.collection_name}' initialized")
            
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            logger.info("Falling back to simple in-memory store")
            self.store = SimpleVectorStore(self.collection_name)
            self.use_chromadb = False
    
    def add_fact(self, fact_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a fact to the vector store."""
        if not self.use_chromadb:
            return self.store.add_fact(fact_id, content, metadata)
        
        try:
            # Prepare metadata
            if metadata is None:
                metadata = {}
            
            # Add to collection
            self.collection.add(
                ids=[fact_id],
                documents=[content],
                metadatas=[metadata]
            )
            return True
        except Exception as e:
            logger.error(f"Error adding fact to vector store: {e}")
            return False
    
    def search_facts(self, query: str, n_results: int = 5, 
                    where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar facts using semantic similarity."""
        if not self.use_chromadb:
            return self.store.search_facts(query, n_results, where)
        
        try:
            # Prepare query parameters
            query_params = {
                "query_texts": [query],
                "n_results": n_results
            }
            
            # Add where filter if provided
            if where:
                query_params["where"] = where
            
            # Execute search
            results = self.collection.query(**query_params)
            
            # Format results
            formatted_results = []
            if results and results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    result = {
                        "id": results['ids'][0][i],
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0.0
                    }
                    formatted_results.append(result)
            
            return formatted_results
        except Exception as e:
            print(f"Error searching facts: {e}")
            return []
    
    def delete_fact(self, fact_id: str) -> bool:
        """Delete a fact from the vector store."""
        if not self.use_chromadb:
            return self.store.delete_fact(fact_id)
        
        try:
            self.collection.delete(ids=[fact_id])
            return True
        except Exception as e:
            print(f"Error deleting fact from vector store: {e}")
            return False
    
    def update_fact(self, fact_id: str, content: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update a fact in the vector store."""
        if not self.use_chromadb:
            return self.store.update_fact(fact_id, content, metadata)
        
        try:
            # ChromaDB doesn't have a direct update method for documents
            # We need to delete and re-add
            self.delete_fact(fact_id)
            return self.add_fact(fact_id, content, metadata)
        except Exception as e:
            print(f"Error updating fact in vector store: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        if not self.use_chromadb:
            return self.store.get_collection_stats()
        
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "count": count,
                "status": "active"
            }
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {
                "collection_name": self.collection_name,
                "count": 0,
                "status": "error",
                "error": str(e)
            }
    
    def reset_collection(self) -> bool:
        """Reset the collection (delete all data)."""
        if not self.use_chromadb:
            return self.store.reset_collection()
        
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            return True
        except Exception as e:
            print(f"Error resetting collection: {e}")
            return False