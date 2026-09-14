from backend.app.memory.behavioral_inference_builder import (
    build_behavioral_inference,
)


tests = [
    (
        "PREFERENCE",
        "I prefer Python.",
    ),
    (
        "USAGE",
        "I frequently use FastAPI.",
    ),
    (
        "LEARNING",
        "I am learning Java.",
    ),
    (
        "INTEREST",
        "I enjoy working with React.",
    ),
    (
        "NEGATIVE PREFERENCE",
        "I don't like Python anymore.",
    ),
    (
        "NEGATIVE USAGE",
        "I stopped using Java.",
    ),
    (
        "NO SIGNAL",
        "I visited Ranchi yesterday.",
    ),
]


print("\n==============================")
print("BEHAVIORAL INFERENCE BUILDER")
print("==============================\n")


for label, text in tests:

    result = build_behavioral_inference(text)

    print(label)
    print("Text      :", text)
    print("Inference :", result)
    print()