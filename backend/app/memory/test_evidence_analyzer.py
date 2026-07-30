from backend.app.models.evidence import Evidence
from backend.app.memory.evidence_analyzer import analyze_evidence


tests = [
    (
        "SUPPORT",
        "I prefer Python.",
        "Python is my favorite programming language."
    ),
    (
        "CONTRADICTION",
        "I prefer Python.",
        "I don't prefer Python anymore."
    ),
    (
        "REFINEMENT",
        "I like Python.",
        "I like Python for AI, but I prefer JavaScript for frontend development."
    ),
    (
        "DUPLICATE",
        "I use Python.",
        "I use Python."
    ),
    (
        "UNRELATED",
        "I prefer Python.",
        "I visited Ranchi yesterday."
    )
]


for expected, old_text, new_text in tests:

    old_evidence = Evidence(
        user_id="user_001",
        content=old_text,
        evidence_type="statement",
        relationship="support",
        reliability=0.90,
        specificity=0.90
    )

    new_evidence = Evidence(
        user_id="user_001",
        content=new_text,
        evidence_type="statement",
        relationship="support",
        reliability=0.90,
        specificity=0.90
    )

    result = analyze_evidence(
        new_evidence,
        [old_evidence]
    )

    print("\n-----------------------------")
    print("EXPECTED:", expected)
    print("OLD:", old_text)
    print("NEW:", new_text)
    print("DETECTED:", result.relationship)
    print("INDEPENDENCE:", round(result.independence, 4))

analyzed = analyze_evidence(
    new_evidence,
    [old_evidence]
)

print("OLD EVIDENCE:")
print(old_evidence.content)

print("\nNEW EVIDENCE:")
print(new_evidence.content)

print("\nINDEPENDENCE SCORE:")
print(round(analyzed.independence, 4))

print("\nSEMANTIC DEPENDENCE:")
print(round(1 - analyzed.independence, 4))