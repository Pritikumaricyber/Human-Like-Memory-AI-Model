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
    emotion=None,
) -> float:
    emotion_bonus = 0.0
    if emotion is not None:
        emotion_bonus = (
            emotion.intensity * 0.04
            + abs(emotion.valence) * 0.03
            + emotion.arousal * 0.03
            )


    score = (
        semantic_similarity * 0.45
        + memory.strength * 0.25
        + memory.importance * 0.15
        + memory.confidence * 0.10
        + emotion_bonus
    )

    return round(
        min(1.0, max(0.0, score)),
        4,
    )


def retrieve_memories(
    query: str,
    memories: list[Memory],
    emotion_store=None,
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
        emotion = None
        if emotion_store is not None:
            emotions = emotion_store.get_by_memory(
                memory.id
                )
            if emotions:
                emotion = emotions[-1]

        score = calculate_retrieval_score(
            similarity,
            memory,
            emotion,
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