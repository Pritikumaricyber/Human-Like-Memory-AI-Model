from datetime import datetime

from backend.app.models.memory import Memory


def decide_forgetting(memory: Memory) -> str:
    """
    Decide whether a memory should remain active,
    become dormant, or be forgotten.

    Rules:
    - Important, emotional, or frequently recalled memories stay active.
    - Old, weak, and rarely recalled memories are forgotten.
    - Everything else becomes dormant.
    """

    age_days = (
        datetime.now() - memory.created_at
    ).days

    # Strong memories remain active
    if (
        memory.importance >= 0.7
        or memory.emotional_score >= 0.7
        or memory.recall_count >= 5
    ):
        return "active"

    # Very weak memories disappear
    if (
        age_days > 90
        and memory.strength < 0.30
        and memory.recall_count <= 1
    ):
        return "forgotten"

    # Otherwise they become dormant
    return "dormant"