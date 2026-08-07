from backend.app.models.memory import Memory
from backend.app.models.emotion import Emotion

from backend.app.memory.dream_priority import (
    calculate_dream_priority,
)

memory = Memory(
    user_id="user_001",
    content="I got my internship.",
    importance=0.80,
    strength=0.75,
)

emotion = Emotion(
    user_id="user_001",
    memory_id=memory.id,
    emotion="joy",
    intensity=0.90,
    valence=0.90,
    arousal=0.80,
)

score = calculate_dream_priority(
    memory,
    emotion,
)

print("\n==============================")
print("DREAM PRIORITY")
print("==============================\n")

print(memory.content)

print()

print("Priority Score:")

print(score)