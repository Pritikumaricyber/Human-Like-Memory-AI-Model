from backend.app.models.evidence import Evidence


evidence = Evidence(
    user_id="user_001",
    content="I use Python for my AI project.",
    evidence_type="behavior",
    relationship="support",
    reliability=0.90,
    specificity=0.85,
    independence=1.0
)

print(evidence.model_dump())