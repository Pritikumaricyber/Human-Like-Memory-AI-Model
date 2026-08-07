from backend.app.models.memory import Memory
from backend.app.models.emotion import Emotion

from backend.app.memory.emotion_engine import apply_emotion


memory = Memory(
    user_id="user_001",
    content="I got my internship.",
    importance=0.50,
    strength=0.50,
    decay_rate=0.02,
)

emotion = Emotion(
    user_id="user_001",
    memory_id=memory.id,
    emotion="joy",
    intensity=0.95,
    valence=0.90,
    arousal=0.90,
)

updated = apply_emotion(
    memory,
    emotion,
)

print("\n==============================")
print("EMOTION ENGINE")
print("==============================\n")

print("Importance :", updated.importance)
print("Strength   :", updated.strength)
print("Decay Rate :", updated.decay_rate)