from backend.app.models.belief import Belief
from backend.app.models.memory import Memory

from backend.app.memory.belief_conflict_detector import (
    detect_belief_conflict,
)


belief = Belief(
    user_id="1",
    subject="Python",
    belief="I like Python.",
)


tests = [
    Memory(
        user_id="1",
        content="I don't like Python.",
    ),
    Memory(
        user_id="1",
        content="I like Python.",
    ),
    Memory(
        user_id="1",
        content="I don't like tea.",
    ),
]


print("\n==============================")
print("BELIEF CONFLICT DETECTOR")
print("==============================\n")

for memory in tests:

    conflict = detect_belief_conflict(
        belief,
        memory,
    )

    print("Belief :", belief.belief)
    print("Memory :", memory.content)
    print("Conflict:", conflict)
    print()