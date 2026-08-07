from datetime import datetime

from backend.app.models.memory import Memory


def calculate_retention(memory: Memory) -> float:
    """
    Calculate how strongly a memory should be retained.

    Returns a score between 0 and 1.
    Higher score = memory should be kept.
    Lower score = memory is a candidate for forgetting.
    """

    # -----------------------------
    # Memory age (days)
    # -----------------------------

    age_days = (
        datetime.now() - memory.created_at
    ).days

    # Older memories lose retention
    age_factor = max(
        0.0,
        1 - (age_days / 365)
    )

    # -----------------------------
    # Recall frequency
    # -----------------------------

    frequency_factor = min(
        memory.frequency / 10,
        1.0,
    )

    # -----------------------------
    # Weighted retention score
    # -----------------------------

    score = (
        memory.importance * 0.25
        + memory.confidence * 0.20
        + memory.strength * 0.25
        + memory.emotional_score * 0.15
        + frequency_factor * 0.10
        + age_factor * 0.05
    )

    return round(
        max(0.0, min(score, 1.0)),
        4,
    )