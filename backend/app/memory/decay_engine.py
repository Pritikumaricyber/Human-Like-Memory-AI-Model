from datetime import datetime


def calculate_decay(
    strength: float,
    decay_rate: float,
    days_since_recall: float
) -> float:
    """
    Calculate memory strength after a period of time.

    Uses exponential decay.
    """

    decayed_strength = strength * (
        2.71828 ** (-decay_rate * days_since_recall)
    )

    return max(
        0.0,
        min(1.0, decayed_strength)
    )


def reinforce_memory(
    strength: float,
    reinforcement: float = 0.15
) -> float:
    """
    Strengthen a memory when it is recalled.
    """

    return min(
        1.0,
        strength + reinforcement
    )
def apply_decay(memory):
    """
    Apply human-like forgetting to a Memory object.

    Memories with high importance, emotion,
    confidence, or recall frequency decay slower.
    """

    if memory.last_recalled is not None:
        days_since = (
            datetime.now() - memory.last_recalled
        ).days
    else:
        days_since = (
            datetime.now() - memory.created_at
        ).days

    # Protection factors
    protection = (
        memory.importance * 0.35
        + memory.emotional_score * 0.25
        + memory.confidence * 0.20
        + min(memory.recall_count, 10) * 0.02
    )

    effective_decay_rate = max(
        0.001,
        memory.decay_rate * (1 - protection)
    )

    memory.strength = calculate_decay(
        strength=memory.strength,
        decay_rate=effective_decay_rate,
        days_since_recall=days_since
    )

    return memory