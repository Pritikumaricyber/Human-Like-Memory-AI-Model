from backend.app.models.evidence import Evidence
from backend.app.embeddings.embedder import generate_embedding
from sklearn.metrics.pairwise import cosine_similarity


def calculate_semantic_similarity(
    text1: str,
    text2: str
) -> float:
    """
    Calculate semantic similarity between two pieces of text.
    """

    embedding1 = generate_embedding(text1)
    embedding2 = generate_embedding(text2)

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )[0][0]

    return float(similarity)


def analyze_evidence(
    evidence: Evidence,
    previous_evidence: list[Evidence]
) -> Evidence:
    """
    Analyze the relationship between new evidence
    and previously stored evidence.
    """

    if not previous_evidence:
        evidence.independence = 1.0
        return evidence

    highest_similarity = 0.0
    relationship = "unrelated"

    for old_evidence in previous_evidence:

        similarity = calculate_semantic_similarity(
            evidence.content,
            old_evidence.content
        )

        if similarity > highest_similarity:
            highest_similarity = similarity

            relationship = classify_relationship(
                old_evidence.content,
                evidence.content,
                similarity
            )

    evidence.independence = max(
        0.0,
        min(1.0, 1.0 - highest_similarity)
    )

    evidence.relationship = relationship

    return evidence

def classify_relationship(
    old_text: str,
    new_text: str,
    similarity: float
) -> str:
    """
    Classify the relationship between two pieces of evidence.

    Current baseline:
    semantic similarity + simple contradiction cues.
    """

    old_lower = old_text.lower()
    new_lower = new_text.lower()

    contradiction_phrases = [
        "don't",
        "do not",
        "doesn't",
        "does not",
        "no longer",
        "stopped",
        "hate",
        "dislike",
        "not anymore",
        "never"
    ]

    has_contradiction_signal = any(
        phrase in new_lower
        for phrase in contradiction_phrases
    )

    if similarity < 0.30:
        return "unrelated"

    if has_contradiction_signal:
        return "contradiction"

    if similarity >= 0.90:
        return "duplicate"

    if similarity >= 0.70:
        return "support"

    return "refinement"