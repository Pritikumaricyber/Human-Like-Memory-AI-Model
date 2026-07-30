from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Belief(BaseModel):
    id: Optional[str] = None
    user_id: str

    subject: str
    belief: str

    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    currentness: float = Field(default=1.0, ge=0.0, le=1.0)

    state: Literal[
        "new",
        "supported",
        "weakened",
        "contested",
        "superseded"
    ] = "new"

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)