from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from uuid import uuid4


class Belief(BaseModel):
    # Identity
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str

    # Belief content
    subject: str
    belief: str

    # Belief strength
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0
    )

    currentness: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0
    )

    # Belief state
    state: Literal[
        "new",
        "supported",
        "weakened",
        "contested",
        "superseded"
    ] = "new"

    # Time
    created_at: datetime = Field(
        default_factory=datetime.now
    )

    updated_at: datetime = Field(
        default_factory=datetime.now
    )