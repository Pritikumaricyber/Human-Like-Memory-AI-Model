from backend.app.memory.behavioral_signal_detector import (
    detect_behavioral_signal,
)

from backend.app.memory.behavioral_concept_extractor import (
    extract_concept,
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
        "USAGE - NATURAL SENTENCE",
        "I usually build AI projects using Python."
    ),
    (
        "LEARNING",
        "I am learning Java."
    ),
    (
        "INTEREST",
        "I enjoy working with React."
    ),
    (
        "NEGATIVE PREFERENCE",
        "I don't like Python anymore."
    ),
    (
        "NEGATIVE USAGE",
        "I stopped using Java."
    ),
]


print("\n==============================")
print("BEHAVIORAL CONCEPT EXTRACTOR")
print("==============================\n")


for label, text in tests:

    signal = detect_behavioral_signal(text)

    if signal is None:
        concept = None
    else:
        concept = extract_concept(
            text,
            signal["matched_phrase"],
        )

    print(label)
    print("Text    :", text)
    print("Concept :", concept)
    print()