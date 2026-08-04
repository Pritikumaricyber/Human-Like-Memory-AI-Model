def calibrate_confidence(
    current_confidence: float,
    conflict: bool,
    learning_rate: float = 0.10,
) -> float:
    """
    Adjust belief confidence based on new evidence.

    Supporting evidence increases confidence.
    Contradicting evidence decreases confidence.
    """

    if conflict:

        current_confidence -= learning_rate

    else:

        current_confidence += learning_rate

    return max(
        0.0,
        min(1.0, current_confidence)
    )