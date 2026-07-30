from backend.app.models.belief_history import BeliefHistory


history = BeliefHistory(
    belief_id="belief_001",
    evidence_id="evidence_001",

    previous_confidence=0.70,
    new_confidence=0.57,

    previous_currentness=1.0,
    new_currentness=0.8785,

    previous_state="supported",
    new_state="contested",

    change_type="contradict"
)


print("BELIEF HISTORY")
print(history.model_dump())