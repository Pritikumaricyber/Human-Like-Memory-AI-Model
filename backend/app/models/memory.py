from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Memory(BaseModel):
    # Identity
    id: Optional[str] = None
    user_id: str

    # Content
    content: str
    memory_type: str = "fact"

    # Human-like memory signals
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    emotional_score: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    frequency: int = Field(default=1, ge=1)

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

    created_at: datetime = Field(default_factory=datetime.now)
    belief_id: str | None = None