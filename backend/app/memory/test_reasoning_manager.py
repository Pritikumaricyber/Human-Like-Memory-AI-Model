from backend.app.models.belief import Belief
from backend.app.models.memory import Memory

from backend.app.memory.reasoning_manager import (
    ReasoningManager,
)


belief = Belief(
    user_id="user_001",
    subject="Programming",
    belief="User prefers Python.",
    confidence=0.75,
)

memory = Memory(
    user_id="user_001",
    content="Python is my favorite language.",
    memory_type="fact",
    importance=0.9,
    confidence=0.9,
    strength=0.8,
)

manager = ReasoningManager()

updated = manager.process_reasoning(
    belief,
    memory,
)

print("\n==============================")
print("REASONING MANAGER")
print("==============================\n")

print("Belief:")
print(updated.belief)

print()

print("Confidence:")
print(updated.confidence)