from uuid import uuid4

from backend.app.models.relationship import Relationship
from backend.app.models.memory import Memory


def build_relationship(
    source: Memory,
    target: Memory,
    relationship_type: str,
    strength: float
) -> Relationship:
    """
    Create a relationship between two memories.
    """

    return Relationship(
        id=str(uuid4()),
        source_id=source.id,
        target_id=target.id,
        relationship_type=relationship_type,
        strength=strength
    )