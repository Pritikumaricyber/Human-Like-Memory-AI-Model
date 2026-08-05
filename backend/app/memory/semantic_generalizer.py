SEMANTIC_MAP = {

    "python": "Programming",

    "fastapi": "Backend Development",
    "flask": "Backend Development",
    "django": "Backend Development",
    "api": "Backend Development",

    "ai": "Artificial Intelligence",
    "machine": "Artificial Intelligence",
    "learning": "Artificial Intelligence",
    "llm": "Artificial Intelligence",
    "tensorflow": "Artificial Intelligence",
    "pytorch": "Artificial Intelligence",

    "ranchi": "Travel",
    "travel": "Travel",
    "trip": "Travel",

    "food": "Food",
    "pizza": "Food",
    "burger": "Food",
    "coffee": "Food",
}


def semantic_generalize(
    clusters: dict[str, list[str]]
) -> dict[str, list[str]]:
    """
    Convert low-level concepts into
    higher-level semantic categories.
    """

    generalized = {}

    for topic, concepts in clusters.items():

        for concept in concepts:

            category = SEMANTIC_MAP.get(
                concept.lower(),
                concept.capitalize()
            )

            if category not in generalized:
                generalized[category] = []

            if concept not in generalized[category]:
                generalized[category].append(concept)

    return generalized