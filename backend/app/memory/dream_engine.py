from backend.app.models.memory import Memory
from backend.app.models.belief import Belief

from backend.app.memory.replay_engine import replay_memories
from backend.app.memory.pattern_detector import detect_patterns
from backend.app.memory.insight_builder import build_insights

from backend.app.storage.emotion_store import EmotionStore


def run_dream_cycle(
    memories: list[Memory],
    user_id: str = "1",
    emotion_store: EmotionStore | None = None,
) -> list[Belief]:
    """
    Simulate an offline dream cycle.

    The AI:
    1. Replays memories using emotional dream priority.
    2. Detects recurring patterns.
    3. Generates new beliefs.
    """

    replayed = replay_memories(
        memories,
        emotion_store=emotion_store,
    )

    patterns = detect_patterns(
        replayed
    )

    insights = build_insights(
        patterns,
        user_id=user_id
    )

    return insights