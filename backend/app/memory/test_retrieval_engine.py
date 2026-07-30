from backend.app.memory.retrieval_engine import (
    calculate_retrieval_score
)


memories = [
    {
        "name": "Python learning",
        "semantic_similarity": 0.92,
        "strength": 0.40,
        "importance": 0.80,
        "currentness": 0.90,
        "emotional_score": 0.30
    },
    {
        "name": "Full-stack goal",
        "semantic_similarity": 0.82,
        "strength": 0.90,
        "importance": 0.95,
        "currentness": 0.95,
        "emotional_score": 0.50
    },
    {
        "name": "Ranchi visit",
        "semantic_similarity": 0.15,
        "strength": 0.95,
        "importance": 0.40,
        "currentness": 0.80,
        "emotional_score": 0.60
    }
]


print("\n==============================")
print("MEMORY RETRIEVAL")
print("==============================")

results = []

for memory in memories:

    score = calculate_retrieval_score(
        semantic_similarity=memory["semantic_similarity"],
        strength=memory["strength"],
        importance=memory["importance"],
        currentness=memory["currentness"],
        emotional_score=memory["emotional_score"]
    )

    results.append(
        (memory["name"], score)
    )


results.sort(
    key=lambda x: x[1],
    reverse=True
)


for rank, (name, score) in enumerate(
    results,
    start=1
):

    print(
        f"{rank}. {name} "
        f"→ Retrieval Score: {score}"
    )