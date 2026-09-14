from backend.app.memory.behavioral_evidence_aggregator import (
    aggregate_behavioral_evidence,
)


tests = [
    (
        "STRONG POSITIVE",
        [
            {"concept": "Python", "direction": "positive"},
            {"concept": "Python", "direction": "positive"},
            {"concept": "Python", "direction": "positive"},
            {"concept": "Python", "direction": "positive"},
        ],
    ),
    (
        "STRONG NEGATIVE",
        [
            {"concept": "Java", "direction": "negative"},
            {"concept": "Java", "direction": "negative"},
            {"concept": "Java", "direction": "negative"},
        ],
    ),
    (
        "CONFLICTED",
        [
            {"concept": "Python", "direction": "positive"},
            {"concept": "Python", "direction": "positive"},
            {"concept": "Python", "direction": "negative"},
            {"concept": "Python", "direction": "negative"},
        ],
    ),
    (
        "MOSTLY POSITIVE",
        [
            {"concept": "React", "direction": "positive"},
            {"concept": "React", "direction": "positive"},
            {"concept": "React", "direction": "positive"},
            {"concept": "React", "direction": "negative"},
        ],
    ),
    (
        "EMPTY",
        [],
    ),
]


print("\n==============================")
print("BEHAVIORAL EVIDENCE AGGREGATOR")
print("==============================\n")


for label, evidence in tests:

    result = aggregate_behavioral_evidence(
        evidence
    )

    print(label)
    print("Evidence    :", evidence)
    print("Aggregation :", result)
    print()