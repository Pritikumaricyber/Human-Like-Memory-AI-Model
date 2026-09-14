def calculate_behavioral_confidence(
    signal_direction: str,
    evidence_count: int = 1,
    base_confidence: float = 0.50,
) -> float:
    """
    Calculate confidence for a behavioral inference.

    Repeated consistent evidence increases confidence.
    Negative evidence starts from the same base but
    represents a negative behavioral direction.
    """

    evidence_count = max(1, evidence_count)

    repetition_bonus = min(
        0.40,
        (evidence_count - 1) * 0.10,
    )

    confidence = base_confidence + repetition_bonus

    return round(
        max(0.0, min(1.0, confidence)),
        4,
    )