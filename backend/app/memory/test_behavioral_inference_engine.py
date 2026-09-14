from backend.app.memory.behavioral_inference_engine import (
    infer_behavior,
)


tests = [
    (
        "PREFERENCE",
        "I prefer Python."
    ),
    (
        "USAGE",
        "I frequently use FastAPI."
    ),
    (
        "LEARNING",
        "I am learning Java."
    ),
    (
        "NEGATIVE PREFERENCE",
        "I don't like Python anymore."
    ),
    (
        "NEGATIVE USAGE",
        "I stopped using Java."
    ),
    (
        "NO SIGNAL",
        "I visited Ranchi yesterday."
    ),
]


print("\n==============================")
print("BEHAVIORAL INFERENCE ENGINE")
print("==============================\n")


for label, text in tests:

    result = infer_behavior(text)

    print(label)
    print("Text      :", text)
    print("Inference :", result)
    print()