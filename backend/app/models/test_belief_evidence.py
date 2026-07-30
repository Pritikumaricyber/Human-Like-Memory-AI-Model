from backend.app.models.belief_evidence import BeliefEvidence


connection = BeliefEvidence(
    belief_id="belief_001",
    evidence_id="evidence_001"
)

print(connection.model_dump())