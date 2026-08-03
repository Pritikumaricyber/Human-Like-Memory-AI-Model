from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Relationship(BaseModel):
    """
    Represents a relationship between two memories or beliefs.
    """

    id: Optional[str] = None

    source_id: str
    target_id: str

    relationship_type: str

    strength: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    updated_at: datetime = Field(
        default_factory=datetime.now
    )