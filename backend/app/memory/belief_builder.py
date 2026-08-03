from backend.app.models.memory import Memory
from backend.app.models.belief import Belief


def build_belief(memory: Memory) -> Belief:
    """
    Build a Belief object from a Memory.
    """

    subject = memory.content.split()[0]

    return Belief(
        user_id=memory.user_id,
        subject=subject,
        belief=memory.content,
        confidence=memory.confidence
    )