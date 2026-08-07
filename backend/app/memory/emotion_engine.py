from backend.app.models.memory import Memory
from backend.app.models.emotion import Emotion


def apply_emotion(
    memory: Memory,
    emotion: Emotion,
) -> Memory:
    """
    Modify memory properties based on emotion.
    """

    # Very strong emotions increase importance
    if emotion.intensity >= 0.80:
        memory.importance = min(
            1.0,
            memory.importance + 0.15,
        )

    # Strong negative emotions are remembered longer
    if emotion.valence < 0:
        memory.strength = min(
            1.0,
            memory.strength + 0.10,
        )

    # High arousal memories decay more slowly
    if emotion.arousal >= 0.80:
        memory.decay_rate *= 0.80

    return memory