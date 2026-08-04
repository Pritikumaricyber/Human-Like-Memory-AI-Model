from backend.app.models.belief import Belief
from backend.app.models.memory import Memory


NEGATIVE_WORDS = {
    "not",
    "don't",
    "dont",
    "never",
    "hate",
    "dislike",
    "avoid",
    "no",
}


def detect_belief_conflict(
    belief: Belief,
    memory: Memory,
) -> bool:
    """
    Detect whether a new memory contradicts
    an existing belief.
    """

    belief_text = belief.belief.lower()
    memory_text = memory.content.lower()

    belief_positive = not any(
        word in belief_text
        for word in NEGATIVE_WORDS
    )

    memory_positive = not any(
        word in memory_text
        for word in NEGATIVE_WORDS
    )

    return belief_positive != memory_positive