from backend.app.models.memory import Memory
from backend.app.memory.replay_engine import replay_memories

memories = [

    Memory(
        user_id="1",
        content="I use Python.",
        strength=0.95,
        importance=0.90
    ),

    Memory(
        user_id="1",
        content="I like tea.",
        strength=0.30,
        importance=0.20
    ),

    Memory(
        user_id="1",
        content="I study AI.",
        strength=0.85,
        importance=0.80
    ),

    Memory(
        user_id="1",
        content="I enjoy FastAPI.",
        strength=0.70,
        importance=0.60
    ),

    Memory(
        user_id="1",
        content="I visited Ranchi.",
        strength=0.40,
        importance=0.30
    )

]

dreams = replay_memories(memories)

print("\n==============================")
print("MEMORY REPLAY")
print("==============================\n")

for memory in dreams:

    print(memory.content)
    print(
        "Strength:",
        memory.strength
    )
    print(
        "Importance:",
        memory.importance
    )
    print()