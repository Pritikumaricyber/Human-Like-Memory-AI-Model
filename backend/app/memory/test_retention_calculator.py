from datetime import datetime, timedelta

from backend.app.models.memory import Memory
from backend.app.memory.retention_calculator import (
    calculate_retention,
)

memory = Memory(
    user_id="user_001",
    content="Python is my favorite language.",
    memory_type="fact",
    importance=0.9,
    confidence=0.9,
    strength=0.8,
    emotional_score=0.3,
)

# Simulate an old memory
memory.created_at = datetime.now() - timedelta(days=30)

score = calculate_retention(memory)

print("\n==============================")
print("RETENTION CALCULATOR")
print("==============================\n")

print("Memory:")
print(memory.content)
print()

print("Retention Score:")
print(score)