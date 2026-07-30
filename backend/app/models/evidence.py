from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Evidence(BaseModel):
    id: Optional[str] = None
    user_id: str

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