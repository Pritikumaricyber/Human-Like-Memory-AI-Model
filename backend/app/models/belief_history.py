from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BeliefHistory(BaseModel):
    """
    Represents one historical state of a belief.

    Every time new evidence changes a belief,
    we can store the previous state here.
    """

    id: Optional[str] = None

    belief_id: str
    evidence_id: Optional[str] = None

    previous_confidence: float = Field(ge=0.0, le=1.0)
    new_confidence: float = Field(ge=0.0, le=1.0)

    previous_currentness: float = Field(ge=0.0, le=1.0)
    new_currentness: float = Field(ge=0.0, le=1.0)

    previous_state: str
    new_state: str

    change_type: str

    created_at: datetime = Field(
        default_factory=datetime.now
    )