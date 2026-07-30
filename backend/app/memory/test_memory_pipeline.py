from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence

from backend.app.memory.memory_pipeline import process_evidence


belief = Belief(
    id="belief_001",
    user_id="user_001",
    subject="user_001",

    belief="User prefers Python",

    confidence=0.70,
    currentness=1.0,

    state="supported"
)


evidence = Evidence(
    id="evidence_001",
    user_id="user_001",

    content="I have started using JavaScript instead.",

    evidence_type="statement",
    relationship="contradict",

    reliability=0.9,
    specificity=0.9,
    independence=1.0
)


print("\n==============================")
print("BEFORE PROCESSING")
print("==============================")

print("Confidence:", belief.confidence)
print("Currentness:", belief.currentness)
print("State:", belief.state)


updated_belief, history = process_evidence(
    belief,
    evidence
)


print("\n==============================")
print("AFTER PROCESSING")
print("==============================")

print("Confidence:", updated_belief.confidence)
print("Currentness:", updated_belief.currentness)
print("State:", updated_belief.state)


print("\n==============================")
print("HISTORY")
print("==============================")

print(history.model_dump())