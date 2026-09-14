from backend.app.models.belief import Belief
from backend.app.embeddings.embedder import generate_embedding
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_MATCH_THRESHOLD = 0.70


def calculate_belief_similarity(
    memory_text: str,
    belief_text: str,
) -> float:
    """
    Calculate semantic similarity between a memory
    and an existing belief.
    """

    memory_embedding = generate_embedding(memory_text)
    belief_embedding = generate_embedding(belief_text)

    similarity = cosine_similarity(
        [memory_embedding],
        [belief_embedding],
    )[0][0]

    return float(similarity)


def find_matching_belief(
    memory_text: str,
    beliefs: list[Belief],
    threshold: float = DEFAULT_MATCH_THRESHOLD,
) -> tuple[Belief | None, float]:
    """
    Find the most semantically similar belief.

    Returns:
        (matching_belief, similarity)

    If no belief reaches the threshold:
        (None, highest_similarity)
    """

    if not beliefs:
        return None, 0.0

    best_belief = None
    best_similarity = 0.0

    for belief in beliefs:

        similarity = calculate_belief_similarity(
            memory_text,
            belief.belief,
        )

        if similarity > best_similarity:

            best_similarity = similarity
            best_belief = belief

    if best_similarity >= threshold:
        return best_belief, best_similarity

    return None, best_similarity