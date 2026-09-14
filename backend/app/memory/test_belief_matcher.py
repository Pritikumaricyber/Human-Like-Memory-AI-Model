from backend.app.models.belief import Belief

from backend.app.memory.belief_matcher import (
    find_matching_belief,
)


beliefs = [

    Belief(
        id="belief_001",
        user_id="user_001",
        subject="Programming",
        belief="User prefers Python.",
        confidence=0.80,
    ),

    Belief(
        id="belief_002",
        user_id="user_001",
        subject="Food",
        belief="User likes tea.",
        confidence=0.70,
    ),

    Belief(
        id="belief_003",
        user_id="user_001",
        subject="Backend",
        belief="User enjoys FastAPI.",
        confidence=0.75,
    ),
]


memories = [

    "Python is my favorite language.",

    "I really like tea.",

    "I enjoy working with FastAPI.",

    "I visited Ranchi yesterday.",
]


print("\n==============================")
print("BELIEF MATCHER")
print("==============================\n")


for memory in memories:

    belief, similarity = find_matching_belief(
        memory,
        beliefs,
    )

    print("Memory :", memory)

    if belief:

        print(
            "Matched belief :",
            belief.belief,
        )

        print(
            "Similarity :",
            round(similarity, 4),
        )

    else:

        print("Matched belief : None")

        print(
            "Highest similarity :",
            round(similarity, 4),
        )

    print()