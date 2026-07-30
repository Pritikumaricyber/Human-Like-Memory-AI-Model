from backend.app.memory.working_memory import WorkingMemory
from backend.app.models.memory import Memory

wm = WorkingMemory(capacity=3)

wm.add(
    Memory(
        user_id="user_001",
        content="I am learning Python.",
        memory_type="fact",
        importance=0.8,
        confidence=0.9,
        strength=0.8,
        emotional_score=0.2,
    )
)

wm.add(
    Memory(
        user_id="user_001",
        content="I want to become an AI Engineer.",
        memory_type="goal",
        importance=0.9,
        confidence=0.9,
        strength=0.8,
        emotional_score=0.6,
    )
)

wm.add(
    Memory(
        user_id="user_001",
        content="I visited Ranchi yesterday.",
        memory_type="event",
        importance=0.4,
        confidence=0.9,
        strength=0.5,
        emotional_score=0.2,
    )
)

print("\nWORKING MEMORY\n")

for memory in wm.retrieve_all():
    print(memory.content)

print("\nSize:", wm.size())