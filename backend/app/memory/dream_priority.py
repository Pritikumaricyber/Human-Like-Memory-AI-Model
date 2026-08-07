from datetime import datetime

from backend.app.models.memory import Memory
from backend.app.models.emotion import Emotion


def calculate_dream_priority(
    memory: Memory,
    emotion: Emotion | None = None,
) -> float:
    """
    Calculate how likely a memory is
    to be replayed during dreaming.
    """

    age_days = (
        datetime.now() - memory.created_at
    ).days

    recency = max(
        0.0,
        1.0 - age_days / 30,
    )

    emotion_bonus = 0.0

    if emotion is not None:

        emotion_bonus = (
            emotion.intensity * 0.20
            + emotion.arousal * 0.10
        )

    priority = (

        memory.importance * 0.35

        + memory.strength * 0.30

        + recency * 0.20

        + emotion_bonus

    )

    return round(
        min(priority, 1.0),
        4,
    )