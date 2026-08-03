from datetime import datetimepython 
from backend.app.models.memory import Memory


def decide_forgetting(memory: Memory) -> str:
    """
    Decide whether a memory should be kept,
    archived, or forgotten.
    """
    from datetime import datetime

from backend.app.models.memory import Memory


def decide_forgetting(memory: Memory) -> str:
    """
    Decide whether a memory should be
    kept, archived, or forgotten.
    """

    age_days = (
        datetime.now() - memory.created_at
    ).days

    if (
        memory.importance >= 0.7
        or memory.emotional_score >= 0.7
        or memory.recall_count >= 5
    ):
        return "keep"

    if (
        age_days > 90
        and memory.strength < 0.30
        and memory.recall_count <= 1
    ):
        return "forget"

    return "archive"