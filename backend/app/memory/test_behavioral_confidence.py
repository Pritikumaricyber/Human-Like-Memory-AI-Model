from backend.app.memory.behavioral_confidence import (
    calculate_behavioral_confidence,
)


tests = [
    ("ONE EVIDENCE", "positive", 1),
    ("TWO EVIDENCE", "positive", 2),
    ("THREE EVIDENCE", "positive", 3),
    ("FOUR EVIDENCE", "positive", 4),
    ("FIVE EVIDENCE", "positive", 5),
    ("NEGATIVE EVIDENCE", "negative", 1),
]


print("\n==============================")
print("BEHAVIORAL CONFIDENCE")
print("==============================\n")


for label, direction, count in tests:

    confidence = calculate_behavioral_confidence(
        signal_direction=direction,
        evidence_count=count,
    )

    print(label)
    print("Direction :", direction)
    print("Evidence  :", count)
    print("Confidence:", confidence)
    print()