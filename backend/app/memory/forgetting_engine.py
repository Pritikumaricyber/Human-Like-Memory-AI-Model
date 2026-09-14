from datetime import datetime

from backend.app.models.memory import Memory


def calculate_memory_retention(
    memory: Memory,
) -> float:
    """
    Calculate how strongly a memory should be retained.

    Retention is influenced by:

    - importance
    - emotional strength
    - confidence
    - recall frequency
    - memory strength
    - recency of recall

    Returns:
        Retention score between 0.0 and 1.0
    """

    now = datetime.now()

    # =========================================================
    # 1. MEMORY AGE
    # =========================================================

    age_days = max(
        0,
        (now - memory.created_at).days,
    )

    # =========================================================
    # 2. RECENCY
    # =========================================================

    if memory.last_recalled is not None:

        days_since_recall = max(
            0,
            (now - memory.last_recalled).days,
        )

    else:

        days_since_recall = age_days

    recency_score = 1.0 / (
        1.0 + days_since_recall / 30.0
    )

    # =========================================================
    # 3. RECALL FREQUENCY
    # =========================================================

    frequency_score = min(
        1.0,
        memory.recall_count / 5.0,
    )

    # =========================================================
    # 4. EMOTIONAL IMPORTANCE
    # =========================================================

    emotional_score = memory.emotional_score

    # =========================================================
    # 5. IMPORTANCE
    # =========================================================

    importance_score = memory.importance

    # =========================================================
    # 6. CONFIDENCE
    # =========================================================

    confidence_score = memory.confidence

    # =========================================================
    # 7. MEMORY STRENGTH
    # =========================================================

    strength_score = memory.strength

    # =========================================================
    # 8. COMBINED RETENTION
    # =========================================================

    retention = (
        0.25 * importance_score
        + 0.20 * emotional_score
        + 0.15 * confidence_score
        + 0.15 * frequency_score
        + 0.15 * strength_score
        + 0.10 * recency_score
    )

    return max(
        0.0,
        min(1.0, retention),
    )


def decide_forgetting(
    memory: Memory,
) -> str:
    """
    Decide the lifecycle state of a memory.

    Possible outcomes:

        active
        dormant
        forgotten

    The decision is primarily based on
    the calculated retention score.

    Important and highly emotional memories
    receive additional protection.
    """

    retention = calculate_memory_retention(
        memory
    )

    # =========================================================
    # 1. IMPORTANT MEMORY
    # =========================================================

    if memory.importance >= 0.70:

        return "active"

    # =========================================================
    # 2. HIGHLY EMOTIONAL MEMORY
    # =========================================================

    if memory.emotional_score >= 0.70:

        return "active"

    # =========================================================
    # 3. STRONG MEMORY
    # =========================================================

    if retention >= 0.70:

        return "active"

    # =========================================================
    # 4. VERY WEAK MEMORY
    # =========================================================

    if retention < 0.20:

        return "forgotten"

    # =========================================================
    # 5. INTERMEDIATE MEMORY
    # =========================================================

    return "dormant"