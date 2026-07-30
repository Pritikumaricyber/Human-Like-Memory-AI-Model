from backend.app.models.memory import Memory
from backend.app.memory.consolidation_engine import consolidate_memory

old_memories = [

    Memory(
        user_id="user_001",
        content="I use Python for AI.",
        memory_type="fact",
        importance=0.8,
        confidence=0.9,
        strength=0.8,
        emotional_score=0.2,
    ),

    Memory(
        user_id="user_001",
        content="I visited Ranchi yesterday.",
        memory_type="event",
        importance=0.5,
        confidence=0.9,
        strength=0.5,
        emotional_score=0.1,
    ),
]

new_memory = Memory(
    user_id="user_001",
    content="Python is my favorite language.",
    memory_type="fact",
    importance=0.8,
    confidence=0.9,
    strength=0.7,
    emotional_score=0.2,
)

results = consolidate_memory(
    new_memory,
    old_memories
)

print("\nMEMORY CONSOLIDATION\n")

for result in results:
    print("----------------------------")
    print("Existing:", result["memory"].content)
    print("Relationship:", result["relationship"])
    print("Independence:", round(result["independence"], 4))