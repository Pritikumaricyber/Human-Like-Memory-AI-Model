from backend.app.models.memory import Memory


memory = Memory(
    user_id="user_001",
    content="I want to become a full-stack developer.",
    memory_type="goal",
    importance=0.85,
    emotional_score=0.4,
    confidence=0.95,
    topics=["React", "JavaScript", "Full Stack"],
)

print(memory.model_dump())