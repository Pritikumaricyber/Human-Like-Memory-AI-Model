from backend.app.models.memory import Memory
from backend.app.models.emotion import Emotion

from backend.app.memory.dream_priority import (
    calculate_dream_priority,
)


def replay_memories(
    memories: list[Memory],
    emotion_store=None,
    top_k: int = 5
) -> list[Memory]:
    """
    Select the strongest memories for dreaming.

    Memories are ranked by strength and importance.
    """

    ranked = []

    for memory in memories:

        emotion = None

        if emotion_store is not None:

            emotions = emotion_store.get_by_memory(
                memory.id
            )

            if emotions:
                emotion = emotions[-1]

        priority = calculate_dream_priority(
            memory,
            emotion,
        )

        ranked.append(
            (
                priority,
                memory,
            )
        )

    ranked.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        memory
        for _, memory in ranked[:top_k]
    ]