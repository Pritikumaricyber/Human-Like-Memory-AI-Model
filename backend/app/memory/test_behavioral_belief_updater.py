from backend.app.models.belief import Belief

from backend.app.memory.behavioral_inference_builder import (
    build_behavioral_inference,
)

from backend.app.memory.behavioral_evidence_builder import (
    build_behavioral_evidence,
)

from backend.app.memory.behavioral_belief_reasoner import (
    reason_about_behavioral_inference,
)

from backend.app.memory.behavioral_belief_updater import (
    update_behavioral_belief,
)


print("\n==============================")
print("BEHAVIORAL BELIEF UPDATER")
print("==============================\n")


# ============================================================
# SUPPORT CASE
# ============================================================

belief = Belief(
    user_id="user_001",
    subject="Programming",
    belief="User prefers Python.",
    confidence=0.70,
)

text = "I prefer Python."

inference = build_behavioral_inference(text)

evidence = build_behavioral_evidence(
    inference=inference,
    confidence=0.70,
)

reasoning_result = reason_about_behavioral_inference(
    belief=belief,
    inference=inference,
)

print("SUPPORT")
print("Original confidence :", belief.confidence)
print("Reasoning result    :", reasoning_result)

updated_belief = update_behavioral_belief(
    belief=belief,
    evidence=evidence,
    reasoning_result=reasoning_result,
)

print("Updated confidence  :", updated_belief.confidence)
print("Updated state       :", updated_belief.state)
print("Currentness         :", updated_belief.currentness)
print()


# ============================================================
# CONTRADICTION CASE
# ============================================================

belief = Belief(
    user_id="user_001",
    subject="Programming",
    belief="User prefers Python.",
    confidence=0.70,
)

text = "I don't like Python anymore."

inference = build_behavioral_inference(text)

evidence = build_behavioral_evidence(
    inference=inference,
    confidence=0.75,
)

reasoning_result = reason_about_behavioral_inference(
    belief=belief,
    inference=inference,
)

print("CONTRADICTION")
print("Original confidence :", belief.confidence)
print("Original currentness:", belief.currentness)
print("Reasoning result    :", reasoning_result)

updated_belief = update_behavioral_belief(
    belief=belief,
    evidence=evidence,
    reasoning_result=reasoning_result,
)

print("Updated confidence  :", updated_belief.confidence)
print("Updated state       :", updated_belief.state)
print("Updated currentness :", updated_belief.currentness)
print()