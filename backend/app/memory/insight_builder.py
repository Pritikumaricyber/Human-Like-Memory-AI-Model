from backend.app.models.belief import Belief


def build_insights(
    patterns: dict[str, int],
    user_id: str = "1"
) -> list[Belief]:
    """
    Convert recurring patterns into new beliefs.
    """

    insights = []

    if patterns.get("python", 0) >= 3:

        insights.append(
            Belief(
                user_id=user_id,
                subject="Programming",
                belief="User prefers Python.",
                confidence=0.75,
                currentness=1.0,
                state="new"
            )
        )

    if patterns.get("ai", 0) >= 2:

        insights.append(
            Belief(
                user_id=user_id,
                subject="Artificial Intelligence",
                belief="User frequently works on AI.",
                confidence=0.70,
                currentness=1.0,
                state="new"
            )
        )

    if patterns.get("fastapi", 0) >= 2:

        insights.append(
            Belief(
                user_id=user_id,
                subject="Backend",
                belief="User enjoys FastAPI development.",
                confidence=0.70,
                currentness=1.0,
                state="new"
            )
        )

    return insights