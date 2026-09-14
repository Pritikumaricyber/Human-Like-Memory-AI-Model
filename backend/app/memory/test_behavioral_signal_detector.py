from backend.app.memory.behavioral_signal_detector import (
    detect_behavioral_signal,
)


tests = [

    (
        "POSITIVE PREFERENCE",
        "I prefer Python.",
    ),

    (
        "POSITIVE FAVORITE",
        "Python is my favorite language.",
    ),

    (
        "POSITIVE INTEREST",
        "I enjoy working with React.",
    ),

    (
        "POSITIVE USAGE",
        "I frequently use FastAPI.",
    ),

    (
        "LEARNING",
        "I am learning Java.",
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
print("BEHAVIORAL SIGNAL DETECTOR")
print("==============================\n")


for label, text in tests:

    result = detect_behavioral_signal(text)

    print(label)
    print("Text   :", text)
    print("Signal :", result)
    print()