from backend.app.memory.behavioral_signal_detector import (
    detect_behavioral_signal,
)


def infer_behavior(
    text: str,
) -> dict | None:
    """
    Infer a behavioral pattern from a memory.

    Returns a structured behavioral inference,
    or None when no behavioral signal is detected.
    """

    signal = detect_behavioral_signal(text)

    if signal is None:
        return None

    signal_type = signal["signal_type"]
    direction = signal["direction"]
    matched_phrase = signal["matched_phrase"]

    if signal_type == "preference":
        behavior = "preference"

    elif signal_type == "usage":
        behavior = "usage"

    elif signal_type == "learning":
        behavior = "learning"

    else:
        behavior = "behavior"

    return {
        "behavior": behavior,
        "direction": direction,
        "matched_phrase": matched_phrase,
        "source_text": text,
    }