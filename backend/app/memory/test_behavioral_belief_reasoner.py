from backend.app.models.belief import Belief

from backend.app.memory.behavioral_inference_builder import (
    build_behavioral_inference,
)

from backend.app.memory.behavioral_belief_reasoner import (
    reason_about_behavioral_inference,
)


belief = Belief(
    user_id="user_001",
    subject="Programming",
    belief="User prefers Python.",
    confidence=0.70,
)


tests = [
    (
        "SUPPORT",
        "I prefer Python.",
    ),
    (
        "CONTRADICTION",
        "I don't like Python anymore.",
    ),
    (
        "UNRELATED",
        "I visited Ranchi yesterday.",
    ),
]


print("\n==============================")
print("BEHAVIORAL BELIEF REASONER")
print("==============================\n")


for label, text in tests:

    inference = build_behavioral_inference(
        text
    )

    print(label)
    print("Text      :", text)
    print("Inference :", inference)

    if inference is None:
        print("Result    : None")
        print()
        continue

    result = reason_about_behavioral_inference(
        belief=belief,
        inference=inference,
    )

    print("Result    :", result)
    print()