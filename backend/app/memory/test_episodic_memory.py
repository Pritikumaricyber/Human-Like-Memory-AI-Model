from backend.app.models.memory import Memory
from backend.app.memory.episodic_memory import EpisodicMemory

episodic = EpisodicMemory()

episodic.add_episode(

    Memory(
        user_id="user_001",
        content="Yesterday I completed my AI project.",
        memory_type="event",
        importance=0.9,
        confidence=1.0,
        strength=0.9,
        emotional_score=0.6,
    )
)

episodic.add_episode(

    Memory(
        user_id="user_001",
        content="I visited Ranchi last week.",
        memory_type="event",
        importance=0.5,
        confidence=1.0,
        strength=0.6,
        emotional_score=0.2,
    )
)

print("\nEPISODIC MEMORY\n")

for episode in episodic.retrieve_all():

    print("------------------------")
    print("Event :", episode["memory"].content)
    print("Time  :", episode["timestamp"])

print("\nTotal Episodes:", episodic.size())