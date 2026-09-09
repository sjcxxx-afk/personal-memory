from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid


@dataclass
class Fact:
    """Represents a single factual memory unit."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""  # The actual fact content
    scene: str = "general"  # Scene tag: work, life, health, etc.
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "chat"  # Source: chat_2026-09-07, note, etc.
    importance: str = "medium"  # high, medium, low
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    temperature: str = "hot"  # hot, warm, cold
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "content": self.content,
            "scene": self.scene,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "importance": self.importance,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "temperature": self.temperature
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Fact':
        """Create Fact from dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            scene=data["scene"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            source=data["source"],
            importance=data["importance"],
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            temperature=data.get("temperature", "hot")
        )


@dataclass
class MemoryPoint:
    """Represents a user profile point derived from facts."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category: str = "preference"  # preference, background, habit, current_state
    content: str = ""  # e.g., "用户喜欢简洁风格"
    evidence: List[str] = field(default_factory=list)  # List of fact IDs supporting this point
    confidence: float = 0.8  # 0-1 confidence score
    last_validated: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "category": self.category,
            "content": self.content,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "last_validated": self.last_validated.isoformat(),
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'MemoryPoint':
        """Create MemoryPoint from dictionary."""
        return cls(
            id=data["id"],
            category=data["category"],
            content=data["content"],
            evidence=data.get("evidence", []),
            confidence=data.get("confidence", 0.8),
            last_validated=datetime.fromisoformat(data["last_validated"]),
            created_at=datetime.fromisoformat(data["created_at"])
        )


@dataclass
class SearchResult:
    """Represents a search result with relevance score."""
    fact: Fact
    score: float = 0.0  # Relevance score (0-1)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API response."""
        return {
            "fact": self.fact.to_dict(),
            "score": self.score
        }