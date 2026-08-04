from collections import Counter

from backend.app.models.memory import Memory


def detect_patterns(
    memories: list[Memory]
) -> dict[str, int]:
    """
    Detect recurring keywords across replayed memories.

    Returns a frequency dictionary.
    """

    counter = Counter()

    for memory in memories:

        words = (
            memory.content.lower()
            .replace(".", "")
            .replace(",", "")
            .split()
        )

        counter.update(words)

    return dict(counter)