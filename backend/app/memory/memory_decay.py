from backend.app.models.memory import Memory


def apply_memory_decay(
    memory: Memory,
    decay_rate: float = 0.02,
) -> Memory:
    """
    Gradually weaken a memory over time.

    The memory is not deleted.
    Only its strength is reduced.

    Returns the updated memory.
    """

    new_strength = max(
        0.0,
        memory.strength - decay_rate,
    )

    memory.strength = round(
        new_strength,
        4,
    )

    return memory