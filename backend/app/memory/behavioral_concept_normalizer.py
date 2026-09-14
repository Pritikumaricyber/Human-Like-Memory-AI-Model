
import re


CONCEPT_SUFFIXES = [
    "projects",
    "project",
    "development",
    "programming",
    "coding",
    "language",
    "technology",
    "technologies",
    "framework",
    "frameworks",
]


def normalize_behavioral_concept(concept: str | None) -> str | None:
    """
    Normalize a behavioral concept into a canonical form.

    The normalization is intentionally conservative so that
    unrelated concepts are not accidentally merged.
    """

    if concept is None:
        return None

    normalized = concept.lower().strip()

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    words = normalized.split()

    while len(words) > 1 and words[-1] in CONCEPT_SUFFIXES:
        words.pop()

    normalized = " ".join(words).strip()

    if not normalized:
        return None

    return normalized
