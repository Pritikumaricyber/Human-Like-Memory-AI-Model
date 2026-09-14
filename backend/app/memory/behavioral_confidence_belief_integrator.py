from backend.app.models.belief import Belief


def apply_behavioral_confidence(
    belief: Belief,
    integrated_confidence: float,
) -> Belief:
    """
    Apply an externally calculated behavioral confidence
    to an existing belief.
    """

    belief.confidence = max(
        0.0,
        min(1.0, integrated_confidence)
    )

    return belief