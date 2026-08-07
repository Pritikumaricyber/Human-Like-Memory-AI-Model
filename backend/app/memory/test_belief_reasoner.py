from backend.app.models.belief import Belief
from backend.app.models.memory import Memory

from backend.app.memory.belief_reasoner import (
    reason_about_belief,
)


belief = Belief(
    user_id="1",
    subject="Python",
    belief="I like Python.",
    confidence=0.8,
)


supporting_memory = Memory(
    user_id="1",
    content="I like Python.",
)


conflicting_memory = Memory(
    user_id="1",
    content="I don't like Python.",
)


print("\n==============================")
print("BELIEF REASONER")
print("==============================\n")


print("SUPPORTING EVIDENCE")

result = reason_about_belief(
    belief,
    supporting_memory,
)

print("Action     :", result["action"])
print("Conflict   :", result["conflict"])
print("Confidence :", result["new_confidence"])
print("State      :", result["state"])


print("\nCONFLICTING EVIDENCE")

result = reason_about_belief(
    belief,
    conflicting_memory,
)

print("Action     :", result["action"])
print("Conflict   :", result["conflict"])
print("Confidence :", result["new_confidence"])
print("State      :", result["state"])