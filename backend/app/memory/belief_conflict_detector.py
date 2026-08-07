from backend.app.models.belief import Belief
from backend.app.models.memory import Memory


NEGATIVE_WORDS = {
    "not",
    "don't",
    "dont",
    "never",
    "hate",
    "hates",
    "dislike",
    "dislikes",
    "avoid",
    "avoids",
    "no",
}


PREFERENCE_WORDS = {
    "like",
    "likes",
    "love",
    "loves",
    "enjoy",
    "enjoys",
    "hate",
    "hates",
    "dislike",
    "dislikes",
    "avoid",
    "avoids",
    "prefer",
    "prefers",
}


def _extract_subject(text: str) -> str | None:
    """
    Extract the object of a simple preference statement.

    Examples:
        I like Python. -> Python
        I don't like Python. -> Python
        I enjoy AI. -> AI
        User prefers Python. -> Python
    """

    words = text.lower().strip().split()

    if not words:
        return None

    for index, word in enumerate(words):

        clean_word = word.strip(".,!?")

        if clean_word in PREFERENCE_WORDS:

            if index + 1 < len(words):

                subject = words[index + 1]

                return subject.strip(".,!?")

    return None


def _is_negative(text: str) -> bool:
    """
    Determine whether a statement expresses
    negative sentiment toward its subject.
    """

    words = text.lower().strip().split()

    for word in words:

        clean_word = word.strip(".,!?")

        if clean_word in NEGATIVE_WORDS:
            return True

    return False


def detect_belief_conflict(
    belief: Belief,
    memory: Memory,
) -> bool:
    """
    Detect whether a new memory contradicts
    an existing belief.

    Conflict requires:

    1. Both statements refer to the same subject.
    2. Their positive/negative polarity differs.
    """

    belief_text = belief.belief.lower()
    memory_text = memory.content.lower()

    # Prefer the actual belief subject only when
    # it represents the object of the preference.
    belief_subject = _extract_subject(
        belief_text
    )

    if belief_subject is None:
        belief_subject = (
            belief.subject.lower().strip()
            if belief.subject
            else None
        )

    memory_subject = _extract_subject(
        memory_text
    )

    # Cannot establish that both statements
    # concern the same subject.
    if (
        belief_subject is None
        or memory_subject is None
    ):
        return False

    if belief_subject != memory_subject:
        return False

    belief_negative = _is_negative(
        belief_text
    )

    memory_negative = _is_negative(
        memory_text
    )

    return belief_negative != memory_negative