from backend.app.memory.behavioral_confidence_integrator import (
    calculate_integrated_confidence,
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
        "MOSTLY POSITIVE",
        [
            {"concept": "React", "direction": "positive"},
            {"concept": "React", "direction": "positive"},
            {"concept": "React", "direction": "positive"},
            {"concept": "React", "direction": "negative"},
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
        "SINGLE EVIDENCE",
        [
            {"concept": "Java", "direction": "positive"},
        ],
    ),
    (
        "EMPTY",
        [],
    ),
]


print("\n==============================")
print("BEHAVIORAL CONFIDENCE INTEGRATOR")
print("==============================\n")


for label, evidence in tests:

    result = calculate_integrated_confidence(
        evidence
    )

    print(label)
    print("Evidence              :", evidence)
    print("Positive count        :", result["positive_count"])
    print("Negative count        :", result["negative_count"])
    print("Consistency           :", result["consistency"])
    print("Net direction         :", result["net_direction"])
    print("Repetition confidence :", result.get(
        "repetition_confidence"
    ))
    print("Final confidence      :", result["confidence"])
    print()