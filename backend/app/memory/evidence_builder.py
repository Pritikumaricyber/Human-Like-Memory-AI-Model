from backend.app.models.memory import Memory
from backend.app.models.evidence import Evidence


def build_evidence(
    memory: Memory,
    relationship: str
) -> Evidence:
    """
    Build an Evidence object from a Memory.
    """

    return Evidence(
        user_id=memory.user_id,
        content=memory.content,

        evidence_type="statement",
        relationship=relationship,

        reliability=memory.confidence,
        specificity=memory.importance,
        independence=1.0
    )