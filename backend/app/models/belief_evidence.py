from pydantic import BaseModel
from datetime import datetime


class BeliefEvidence(BaseModel):
    belief_id: str
    evidence_id: str

    created_at: datetime = datetime.now()