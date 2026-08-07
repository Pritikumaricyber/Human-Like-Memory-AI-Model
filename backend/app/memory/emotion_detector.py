from backend.app.models.emotion import Emotion


EMOTION_RULES = {
    "joy": [
        "happy",
        "joy",
        "love",
        "excited",
        "promotion",
        "won",
        "success",
        "internship",
        "favorite",
    ],
    "sadness": [
        "sad",
        "cry",
        "lost",
        "failure",
        "fail",
        "alone",
    ],
    "fear": [
        "fear",
        "scared",
        "afraid",
        "danger",
        "accident",
        "exam",
    ],
    "anger": [
        "angry",
        "furious",
        "hate",
        "annoyed",
        "frustrated",
    ],
}


EMOTION_VALUES = {
    "joy": (0.90, 0.90, 0.80),
    "sadness": (0.80, -0.80, 0.40),
    "fear": (0.95, -0.90, 0.95),
    "anger": (0.90, -0.85, 0.90),
}


def detect_emotion(
    user_id: str,
    memory_id: str,
    text: str,
) -> Emotion:
    """
    Detect the dominant emotion from text
    using a simple rule-based approach.
    """

    lower_text = text.lower()

    for emotion, keywords in EMOTION_RULES.items():

        for keyword in keywords:

            if keyword in lower_text:

                intensity, valence, arousal = EMOTION_VALUES[
                    emotion
                ]

                return Emotion(
                    user_id=user_id,
                    memory_id=memory_id,
                    emotion=emotion,
                    intensity=intensity,
                    valence=valence,
                    arousal=arousal,
                )

    return Emotion(
        user_id=user_id,
        memory_id=memory_id,
        emotion="neutral",
        intensity=0.20,
        valence=0.0,
        arousal=0.20,
    )