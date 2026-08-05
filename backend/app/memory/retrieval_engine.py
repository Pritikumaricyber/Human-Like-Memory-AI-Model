import numpy as np

from backend.app.embeddings.embedder import generate_embedding
from backend.app.models.memory import Memory


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:

    a = np.array(vector_a)
    b = np.array(vector_b)

    denominator = (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(a, b) / denominator
    )


def calculate_retrieval_score(
    semantic_similarity: float,
    memory: Memory,
) -> float:

    score = (
        semantic_similarity * 0.45
        + memory.strength * 0.25
        + memory.importance * 0.15
        + memory.confidence * 0.10
        + memory.emotional_score * 0.05
    )

    return round(
        min(1.0, max(0.0, score)),
        4,
    )


def retrieve_memories(
    query: str,
    memories: list[Memory],
    top_k: int = 5,
):

    query_embedding = generate_embedding(query)

    results = []

    for memory in memories:

        if memory.embedding is None:
            memory.embedding = generate_embedding(
                memory.content
            )

        similarity = cosine_similarity(
            query_embedding,
            memory.embedding,
        )

        score = calculate_retrieval_score(
            similarity,
            memory,
        )

        results.append(
            {
                "memory": memory,
                "semantic_similarity": round(
                    similarity,
                    4,
                ),
                "retrieval_score": score,
            }
        )

    results.sort(
        key=lambda item: item["retrieval_score"],
        reverse=True,
    )

    return results[:top_k]