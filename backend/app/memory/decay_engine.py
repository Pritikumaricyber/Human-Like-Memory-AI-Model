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
    Apply decay directly to a Memory object.
    """

    if memory.last_recalled is not None:
        days_since = (
            datetime.now() - memory.last_recalled
        ).days
    else:
        days_since = (
            datetime.now() - memory.created_at
        ).days

    memory.strength = calculate_decay(
        strength=memory.strength,
        decay_rate=memory.decay_rate,
        days_since_recall=days_since
    )

    return memory