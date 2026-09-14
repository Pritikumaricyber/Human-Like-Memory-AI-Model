import re


# ============================================================
# POSITIVE SIGNALS
# ============================================================

POSITIVE_SIGNALS = {
    "preference": [
        "prefer",
        "prefers",
        "favorite",
        "favourite",
        "love",
        "loves",
        "like",
        "likes",
        "enjoy",
        "enjoys",
    ],
    "usage": [
        "use",
        "uses",
        "using",
        "usually use",
        "often use",
        "frequently use",
    ],
    "learning": [
        "learn",
        "learning",
        "studying",
        "study",
        "practice",
        "practicing",
    ],
}


# ============================================================
# NEGATIVE SIGNALS
# ============================================================

NEGATIVE_SIGNALS = {
    "preference": [
        "hate",
        "hates",
        "dislike",
        "dislikes",
        "don't like",
        "do not like",
        "doesn't like",
        "does not like",
        "don't prefer",
        "do not prefer",
        "doesn't prefer",
        "does not prefer",
        "no longer like",
        "no longer prefer",
    ],
    "usage": [
        "stopped using",
        "no longer use",
        "don't use",
        "do not use",
    ],
}


# ============================================================
# SIGNAL DETECTION
# ============================================================

def detect_behavioral_signal(
    text: str,
) -> dict | None:
    """
    Detect a behavioral signal from a memory.

    Returns:
        {
            "signal_type": ...,
            "direction": ...,
            "matched_phrase": ...
        }

    Returns None when no behavioral signal is detected.
    """

    text_lower = text.lower().strip()

    # --------------------------------------------------------
    # 1. Negative signals
    # --------------------------------------------------------

    for signal_type, phrases in NEGATIVE_SIGNALS.items():
        for phrase in sorted(
            phrases,
            key=len,
            reverse=True,
            ):
            if re.search(
                rf"\b{re.escape(phrase)}\b",
                text_lower,
                ):
                return {
                    "signal_type": signal_type,
                    "direction": "negative",
                    "matched_phrase": phrase,
                    }
    # --------------------------------------------------------
    # 2. Positive signals
    # --------------------------------------------------------

    for signal_type, phrases in POSITIVE_SIGNALS.items():
        for phrase in sorted(
            phrases,
            key=len,
            reverse=True,
            ):
            if re.search(
                rf"\b{re.escape(phrase)}\b",
                text_lower,
                ):
                return {
                    "signal_type": signal_type,
                    "direction": "positive",
                    "matched_phrase": phrase,
                    }

    return None