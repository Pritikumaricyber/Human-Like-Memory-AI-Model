from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence

from backend.app.memory.belief_history_manager import (
    record_belief_change,
    add_history
)


# -----------------------------
# OLD BELIEF
# -----------------------------

old_belief = Belief(
    id="belief_001",
    user_id="user_001",
    subject="user_001",
    belief="User prefers Python",

    confidence=0.70,
    currentness=1.0,

    state="supported"
)


# -----------------------------
# NEW BELIEF
# -----------------------------

new_belief = Belief(
    id="belief_001",
    user_id="user_001",
    subject="user_001",
    belief="User prefers Python",

    confidence=0.57,
    currentness=0.8785,

    state="contested"
)


# -----------------------------
# EVIDENCE
# -----------------------------

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


# -----------------------------
# CREATE HISTORY RECORD
# -----------------------------

record = record_belief_change(
    old_belief,
    new_belief,
    evidence
)


# -----------------------------
# STORE RECORD
# -----------------------------

history = []

history = add_history(
    history,
    record
)


print("\nBELIEF HISTORY RECORD")
print(record.model_dump())

print("\nTOTAL HISTORY RECORDS")
print(len(history))