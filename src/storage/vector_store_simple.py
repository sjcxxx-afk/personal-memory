"""
Simple in-memory vector store for testing purposes.
This is a simplified version that doesn't require ChromaDB.
"""

from typing import List, Optional, Dict, Any
import re
from collections import defaultdict


class SimpleVectorStore:
    """Simple in-memory vector store using text matching."""
    
    def __init__(self, collection_name: str = "facts"):
        self.collection_name = collection_name
        self.documents = {}  # fact_id -> document content
        self.metadata = {}   # fact_id -> metadata
        self.inverted_index = defaultdict(set)  # word -> set of fact_ids
        
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization: split by whitespace and lowercase, with support for Chinese characters."""
        # For Chinese: split into individual characters and words
        # For English: split by whitespace and lowercase
        tokens = []
        
        # Split by whitespace first
        words = text.split()
        for word in words:
            # Lowercase for English
            word = word.lower()
            
            # Check if word contains Chinese characters
            if re.search(r'[\u4e00-\u9fff]', word):
                # Chinese: add individual characters and the whole word
                tokens.append(word)
                # Also add individual Chinese characters for matching
                for char in word:
                    if re.search(r'[\u4e00-\u9fff]', char):
                        tokens.append(char)
            else:
                # English: add the whole word
                tokens.append(word)
        
        return tokens
    
    def add_fact(self, fact_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add a fact to the store."""
        try:
            # Store document and metadata
            self.documents[fact_id] = content
            self.metadata[fact_id] = metadata or {}
            
            # Update inverted index
            tokens = self._tokenize(content)
            for token in tokens:
                self.inverted_index[token].add(fact_id)
            
            return True
        except Exception as e:
            print(f"Error adding fact: {e}")
            return False
    
    def search_facts(self, query: str, n_results: int = 5, 
                    where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for facts using text matching."""
        try:
            # Tokenize query
            query_tokens = self._tokenize(query)
            
            if not query_tokens:
                return []
            
            # Find matching fact IDs using inverted index
            matching_ids = None
            for token in query_tokens:
                if token in self.inverted_index:
                    if matching_ids is None:
                        matching_ids = self.inverted_index[token].copy()
                    else:
                        matching_ids &= self.inverted_index[token]
            
            if not matching_ids:
                # If no exact matches, try partial matching
                matching_ids = set()
                for token in query_tokens:
                    for word, ids in self.inverted_index.items():
                        if token in word or word in token:
                            matching_ids.update(ids)
            
            if not matching_ids:
                return []
            
            # Apply metadata filter if provided
            if where:
                filtered_ids = set()
                for fact_id in matching_ids:
                    fact_metadata = self.metadata.get(fact_id, {})
                    match = True
                    for key, value in where.items():
                        if fact_metadata.get(key) != value:
                            match = False
                            break
                    if match:
                        filtered_ids.add(fact_id)
                matching_ids = filtered_ids
            
            # Calculate simple relevance scores
            results = []
            for fact_id in matching_ids:
                content = self.documents[fact_id]
                # Simple scoring: count matching tokens
                content_tokens = set(self._tokenize(content))
                query_tokens_set = set(query_tokens)
                overlap = len(content_tokens & query_tokens_set)
                score = overlap / len(query_tokens_set) if query_tokens_set else 0
                
                results.append({
                    "id": fact_id,
                    "content": content,
                    "metadata": self.metadata.get(fact_id, {}),
                    "distance": 1.0 - score  # Convert to distance (lower is better)
                })
            
            # Sort by distance (lower is better)
            results.sort(key=lambda x: x["distance"])
            
            # Return top N results
            return results[:n_results]
            
        except Exception as e:
            print(f"Error searching facts: {e}")
            return []
    
    def delete_fact(self, fact_id: str) -> bool:
        """Delete a fact from the store."""
        try:
            if fact_id in self.documents:
                # Remove from inverted index
                content = self.documents[fact_id]
                tokens = self._tokenize(content)
                for token in tokens:
                    if token in self.inverted_index:
                        self.inverted_index[token].discard(fact_id)
                
                # Remove from storage
                del self.documents[fact_id]
                if fact_id in self.metadata:
                    del self.metadata[fact_id]
                
                return True
            return False
        except Exception as e:
            print(f"Error deleting fact: {e}")
            return False
    
    def update_fact(self, fact_id: str, content: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update a fact in the store."""
        try:
            # Delete old version
            self.delete_fact(fact_id)
            # Add new version
            return self.add_fact(fact_id, content, metadata)
        except Exception as e:
            print(f"Error updating fact: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        return {
            "collection_name": self.collection_name,
            "count": len(self.documents),
            "status": "active",
            "index_size": len(self.inverted_index)
        }
    
    def reset_collection(self) -> bool:
        """Reset the collection (delete all data)."""
        try:
            self.documents.clear()
            self.metadata.clear()
            self.inverted_index.clear()
            return True
        except Exception as e:
            print(f"Error resetting collection: {e}")
            return False