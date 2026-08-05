from backend.app.models.belief import Belief


def generalize(
    semantic_clusters: dict[str, list[str]],
    user_id: str,
) -> list[Belief]:
    """
    Convert semantic concept clusters
    into long-term beliefs.
    """

    beliefs = []

    belief_templates = {

        "Programming":
            "User has strong programming experience.",

        "Backend Development":
            "User frequently develops backend applications.",

        "Artificial Intelligence":
            "User frequently works on AI.",

        "Travel":
            "User often travels to different places.",

        "Web Development":
            "User has experience building web applications.",

        "Data Science":
            "User frequently works with data science concepts.",
    }

    for subject, concepts in semantic_clusters.items():

        if not concepts:
            continue

        belief_text = belief_templates.get(
            subject,
            f"User has recurring experience with {subject.lower()}."
        )

        confidence = min(
            0.70 + len(concepts) * 0.05,
            0.95,
        )

        beliefs.append(

            Belief(
                user_id=user_id,
                subject=subject,
                belief=belief_text,
                confidence=confidence,
                state="new",
            )

        )

    return beliefs