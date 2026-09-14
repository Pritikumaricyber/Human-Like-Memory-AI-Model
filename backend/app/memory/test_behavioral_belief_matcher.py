from backend.app.models.belief import Belief

from backend.app.memory.behavioral_inference_builder import (
    build_behavioral_inference,
)

from backend.app.memory.behavioral_belief_matcher import (
    match_behavioral_belief,
)


beliefs = [
    Belief(
        user_id="user_001",
        subject="Programming",
        belief="User prefers Python.",
        confidence=0.70,
    ),
    Belief(
        user_id="user_001",
        subject="Backend",
        belief="User enjoys FastAPI development.",
        confidence=0.70,
    ),
    Belief(
        user_id="user_001",
        subject="Learning",
        belief="User is learning Java.",
        confidence=0.60,
    ),
]


tests = [
    (
        "PYTHON PREFERENCE",
        "I prefer Python.",
    ),
    (
        "FASTAPI USAGE",
        "I frequently use FastAPI.",
    ),
    (
        "JAVA LEARNING",
        "I am learning Java.",
    ),
    (
        "UNRELATED",
        "I visited Ranchi yesterday.",
    ),
]


print("\n==============================")
print("BEHAVIORAL BELIEF MATCHER")
print("==============================\n")


for label, text in tests:

    inference = build_behavioral_inference(
        text
    )

    print(label)
    print("Text      :", text)
    print("Inference :", inference)

    belief, similarity = match_behavioral_belief(
        inference=inference,
        beliefs=beliefs,
    )

    if belief is None:
        print("Matched   : None")
    else:
        print("Matched   :", belief.belief)

    print(
        "Similarity:",
        round(similarity, 4),
    )

    print()