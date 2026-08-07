from backend.app.models.memory import Memory
from backend.app.memory.memory_decay import (
    apply_memory_decay,
)

memory = Memory(
    user_id="user_001",
    content="Python is my favorite language.",
    memory_type="fact",
    importance=0.9,
    confidence=0.9,
    strength=0.80,
    emotional_score=0.2,
)

print("\n==============================")
print("MEMORY DECAY")
print("==============================\n")

print("Initial Strength:")
print(memory.strength)
print()

for day in range(1, 6):

    apply_memory_decay(memory)

    print(
        f"Day {day}:",
        memory.strength,
    )