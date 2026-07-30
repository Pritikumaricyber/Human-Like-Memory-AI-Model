from datetime import datetime, timedelta

from backend.app.models.memory import Memory
from backend.app.memory.memory_scheduler import run_memory_scheduler


memories = [

    Memory(
        user_id="user_001",
        content="I am learning Python.",
        memory_type="fact",
        importance=0.8,
        confidence=0.9,
        strength=0.8,
        emotional_score=0.2,
        created_at=datetime.now() - timedelta(days=30),
    ),

    Memory(
        user_id="user_001",
        content="I visited Ranchi.",
        memory_type="event",
        importance=0.4,
        confidence=0.9,
        strength=0.6,
        emotional_score=0.1,
        created_at=datetime.now() - timedelta(days=60),
    ),
]

print("\nBEFORE\n")

for memory in memories:
    print(memory.content)
    print("Strength:", round(memory.strength, 4))
    print()

updated = run_memory_scheduler(memories)

print("\nAFTER\n")

for memory in updated:
    print(memory.content)
    print("Strength :", round(memory.strength, 4))
    print("Status   :", memory.status)
    print()