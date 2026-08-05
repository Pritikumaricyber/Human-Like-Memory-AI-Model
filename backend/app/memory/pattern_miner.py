from collections import Counter

from backend.app.models.memory import Memory


def mine_patterns(
    episodes: dict[str, list[Memory]]
) -> dict[str, Counter]:
    """
    Mine repeated concepts from grouped episodes.

    Returns a Counter of words for every episode group.
    """

    patterns = {}

    for topic, memories in episodes.items():

        counter = Counter()

        for memory in memories:

            words = memory.content.lower().split()

            counter.update(words)

        patterns[topic] = counter

    return patterns