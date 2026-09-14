from backend.app.models.belief import Belief

from backend.app.memory.belief_matcher import (
    find_matching_belief,
)


def match_behavioral_belief(
    inference: dict,
    beliefs: list[Belief],
    threshold: float = 0.70,
) -> tuple[Belief | None, float]:
    """
    Match a behavioral inference against existing beliefs.

    The existing belief matcher performs the actual
    semantic comparison. This function only adapts
    the behavioral inference to that interface.
    """

    if inference is None:
        return None, 0.0

    inference_text = inference["inference"]

    return find_matching_belief(
        memory_text=inference_text,
        beliefs=beliefs,
        threshold=threshold,
    )