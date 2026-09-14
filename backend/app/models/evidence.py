from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import uuid4


class Evidence(BaseModel):
    id: str = Field(
    default_factory=lambda: str(uuid4())
)
    user_id: str

    belief_id: Optional[str] = None

    content: str

    evidence_type: Literal[
        "statement",
        "behavior",
        "event",
        "inference"
    ]

    relationship: Literal[
    "support",
    "contradict",
    "refinement",
    "duplicate",
    "context",
    "unrelated"
]

    reliability: float = Field(default=0.5, ge=0.0, le=1.0)
    specificity: float = Field(default=0.5, ge=0.0, le=1.0)
    independence: float = Field(default=1.0, ge=0.0, le=1.0)

    created_at: datetime = Field(default_factory=datetime.now)