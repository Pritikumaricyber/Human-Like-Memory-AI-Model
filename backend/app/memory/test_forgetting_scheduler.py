from datetime import datetime, timedelta

from backend.app.models.memory import Memory
from backend.app.memory.forgetting_scheduler import (
    run_forgetting_scheduler,
)

memories = [

    Memory(
        user_id="1",
        content="Python is my favorite language.",
        importance=0.9,
        emotional_score=0.8,
        confidence=0.9,
        strength=0.95,
        decay_rate=0.01,
        recall_count=10,
        created_at=datetime.now() - timedelta(days=180),
    ),

    Memory(
        user_id="1",
        content="I ate noodles.",
        importance=0.2,
        emotional_score=0.1,
        confidence=0.3,
        strength=0.45,
        decay_rate=0.02,
        recall_count=1,
        created_at=datetime.now() - timedelta(days=180),
    ),

    Memory(
        user_id="1",
        content="Visited the library.",
        importance=0.5,
        emotional_score=0.2,
        confidence=0.7,
        strength=0.70,
        decay_rate=0.01,
        recall_count=3,
        created_at=datetime.now() - timedelta(days=60),
    ),
]

updated = run_forgetting_scheduler(memories)

print("\n==============================")
print("HUMAN-LIKE FORGETTING")
print("==============================\n")

for memory in updated:

    print(memory.content)
    print("Strength :", round(memory.strength, 4))
    print("Status   :", memory.status)
    print()