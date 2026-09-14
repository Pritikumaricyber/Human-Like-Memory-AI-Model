from backend.app.memory.behavioral_inference_builder import (
    build_behavioral_inference,
)

from backend.app.memory.behavioral_evidence_builder import (
    build_behavioral_evidence,
)


tests = [
    (
        "POSITIVE PREFERENCE",
        "I prefer Python.",
        0.70,
    ),
    (
        "POSITIVE USAGE",
        "I frequently use FastAPI.",
        0.80,
    ),
    (
        "POSITIVE LEARNING",
        "I am learning Java.",
        0.60,
    ),
    (
        "NEGATIVE PREFERENCE",
        "I don't like Python anymore.",
        0.75,
    ),
    (
        "NEGATIVE USAGE",
        "I stopped using Java.",
        0.65,
    ),
]


print("\n==============================")
print("BEHAVIORAL EVIDENCE BUILDER")
print("==============================\n")


for label, text, confidence in tests:

    inference = build_behavioral_inference(
        text
    )

    if inference is None:
        print(label)
        print("Inference : None")
        print()
        continue

    inference["user_id"] = "user_001"

    evidence = build_behavioral_evidence(
        inference=inference,
        confidence=confidence,
    )

    print(label)
    print("Inference :", inference)
    print("Evidence  :", evidence)
    print()