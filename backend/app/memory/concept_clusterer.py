from collections import defaultdict

STOP_WORDS = {
    "is",
    "am",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "the",
    "a",
    "an",
    "to",
    "of",
    "and",
    "for",
    "in",
    "on",
    "at",
    "has",
    "have",
    "had",
}


def cluster_concepts(
    patterns: dict
) -> dict[str, list[str]]:
    """
    Convert mined patterns into concepts.

    Common stop words are ignored.
    """

    clusters = defaultdict(list)

    for topic, counter in patterns.items():

        for word, frequency in counter.items():

            if (
                frequency >= 2
                and word not in STOP_WORDS
            ):
                clusters[topic].append(word)

    return dict(clusters)