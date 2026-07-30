from backend.app.models.memory import Memory
from backend.app.memory.reconsolidation_engine import (
    reconsolidate_memory,
)

memory = Memory(
    user_id="user_001",
    content="I use Python for AI.",
    memory_type="fact",
    importance=0.8,
    confidence=0.85,
    strength=0.70,
    emotional_score=0.2,
)

print("\nBEFORE RECONSOLIDATION\n")

print("Content       :", memory.content)
print("Confidence    :", memory.confidence)
print("Strength      :", memory.strength)
print("Recall Count  :", memory.recall_count)
print("Last Recalled :", memory.last_recalled)

updated_memory = reconsolidate_memory(
    memory,
    "I use Python for AI and backend development."
)

print("\nAFTER RECONSOLIDATION\n")

print("Content       :", updated_memory.content)
print("Confidence    :", updated_memory.confidence)
print("Strength      :", updated_memory.strength)
print("Recall Count  :", updated_memory.recall_count)
print("Last Recalled :", updated_memory.last_recalled)