from backend.app.models.memory import Memory
from backend.app.memory.retrieval_engine import (
    retrieve_memories
)
from backend.app.embeddings.embedder import generate_embedding


memory_contents = [
    (
        "I am learning Python for AI.",
        "goal",
        0.85,
        0.40,
        0.90
    ),
    (
        "I want to become a full-stack developer.",
        "goal",
        0.95,
        0.50,
        0.95
    ),
    (
        "I visited Ranchi yesterday.",
        "experience",
        0.40,
        0.60,
        0.80
    )
]


memories = []


for index, (
    content,
    memory_type,
    importance,
    emotional_score,
    currentness
) in enumerate(memory_contents):

    embedding = generate_embedding(content)

    memory = Memory(
        id=f"memory_{index + 1}",
        user_id="user_001",
        content=content,
        memory_type=memory_type,
        importance=importance,
        emotional_score=emotional_score,
        confidence=0.9,
        frequency=1,
        strength=0.7,
        decay_rate=0.01,
        currentness=currentness,
        embedding=embedding.tolist()
    )

    memories.append(memory)


query = "What am I learning for AI?"


print("\n==============================")
print("QUERY")
print("==============================")

print(query)


results = retrieve_memories(
    query,
    memories,
    top_k=3
)


print("\n==============================")
print("RETRIEVED MEMORIES")
print("==============================")


for rank, result in enumerate(
    results,
    start=1
):

    memory = result["memory"]

    print(
        f"\n{rank}. {memory.content}"
    )

    print(
        "Semantic Similarity:",
        result["semantic_similarity"]
    )

    print(
        "Retrieval Score:",
        result["retrieval_score"]
    )
