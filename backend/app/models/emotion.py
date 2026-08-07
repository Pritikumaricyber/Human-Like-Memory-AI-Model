from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class Emotion(BaseModel):
    """
    Represents the emotional state
    associated with a memory.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    user_id: str

    memory_id: str

    emotion: str

    intensity: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )

    valence: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
    )

    arousal: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )