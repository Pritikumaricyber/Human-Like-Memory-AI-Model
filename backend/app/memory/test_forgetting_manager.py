from datetime import datetime, timedelta

from backend.app.models.memory import Memory
from backend.app.memory.forgetting_manager import ForgettingManager


manager = ForgettingManager()

memories = [

    Memory(
        user_id="user_001",
        content="Python",
        importance=0.9,
        emotional_score=0.8,
        confidence=0.9,
        strength=0.9,
        recall_count=10,
    ),

    Memory(
        user_id="user_001",
        content="College Bus",
        importance=0.3,
        emotional_score=0.1,
        confidence=0.6,
        strength=0.4,
        recall_count=2,
        created_at=datetime.now() - timedelta(days=40),
    ),

    Memory(
        user_id="user_001",
        content="Random Number",
        importance=0.1,
        emotional_score=0.0,
        confidence=0.3,
        strength=0.2,
        recall_count=0,
        created_at=datetime.now() - timedelta(days=150),
    ),
]

print("\n==============================")
print("FORGETTING MANAGER")
print("==============================\n")

for memory in memories:

    updated = manager.process_memory(memory)

    print(updated.content)
    print("Status   :", updated.status)
    print("Strength :", updated.strength)
    print()