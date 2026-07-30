from backend.app.models.memory import Memory
from backend.app.memory.decision_engine import decide_memory_action

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
    content="Python is my favorite programming language.",
    memory_type="fact",
    importance=0.8,
    confidence=0.9,
    strength=0.8,
    emotional_score=0.2,
)

decision = decide_memory_action(
    new_memory,
    old_memories
)

print("\nMEMORY DECISION\n")

print("Action       :", decision["action"])
print("Relationship :", decision["relationship"])
print("Target       :", decision["target"].content)
print("Independence :", round(decision["independence"], 4))