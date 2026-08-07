from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from uuid import uuid4

class Memory(BaseModel):
    # Identity
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str

    # Content
    content: str
    memory_type: str = "fact"

    # Human-like memory signals
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    emotional_score: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    frequency: int = Field(default=0, ge=0)

    # Memory lifecycle
    strength: float = Field(default=0.5, ge=0.0, le=1.0)
    decay_rate: float = Field(default=0.01, ge=0.0, le=1.0)

    # Time
    created_at: datetime = Field(default_factory=datetime.now)
    last_recalled: Optional[datetime] = None

    # Relationships
    topics: List[str] = Field(default_factory=list)
    entities: List[str] = Field(default_factory=list)
    related_memories: List[str] = Field(default_factory=list)

    # Lifecycle status
    status: str = "active"

    embedding: list[float] | None = None

    recall_count: int = 0

    
    belief_id: str | None = None