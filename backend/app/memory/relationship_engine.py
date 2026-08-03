from backend.app.models.memory import Memory


def detect_relationship(
    memory1: Memory,
    memory2: Memory
) -> tuple[str, float]:
    """
    Detect the relationship between two memories.
    """

    words1 = set(memory1.content.lower().split())
    words2 = set(memory2.content.lower().split())

    common = words1.intersection(words2)

    if not common:
        return "unrelated", 0.0

    strength = len(common) / max(
        len(words1),
        len(words2)
    )

    return "related", strength