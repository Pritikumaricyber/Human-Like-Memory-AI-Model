from backend.app.models.memory import Memory


def replay_memories(
    memories: list[Memory],
    top_k: int = 5
) -> list[Memory]:
    """
    Select the strongest memories for dreaming.

    Memories are ranked by strength and importance.
    """

    ranked = sorted(
        memories,
        key=lambda m: (
            m.strength,
            m.importance
        ),
        reverse=True
    )

    return ranked[:top_k]