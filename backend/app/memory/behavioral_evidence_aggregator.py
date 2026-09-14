def aggregate_behavioral_evidence(
    evidence: list[dict],
) -> dict:
    """
    Aggregate behavioral evidence for a concept.

    Each evidence item should contain:
        {
            "concept": str,
            "direction": "positive" | "negative"
        }
    """

    if not evidence:
        return {
            "concept": None,
            "positive_count": 0,
            "negative_count": 0,
            "total_count": 0,
            "consistency": 0.0,
            "net_direction": None,
        }

    concept = evidence[0].get("concept")

    positive_count = sum(
        1
        for item in evidence
        if item.get("direction") == "positive"
    )

    negative_count = sum(
        1
        for item in evidence
        if item.get("direction") == "negative"
    )

    total_count = (
        positive_count
        + negative_count
    )

    if total_count == 0:
        return {
            "concept": concept,
            "positive_count": 0,
            "negative_count": 0,
            "total_count": 0,
            "consistency": 0.0,
            "net_direction": None,
        }

    consistency = abs(
        positive_count - negative_count
    ) / total_count

    if positive_count > negative_count:
        net_direction = "positive"

    elif negative_count > positive_count:
        net_direction = "negative"

    else:
        net_direction = "conflicted"

    return {
        "concept": concept,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "total_count": total_count,
        "consistency": round(consistency, 4),
        "net_direction": net_direction,
    }