
from backend.app.models.belief import Belief


MIN_BEHAVIORAL_EVIDENCE = 2
REINFORCEMENT_RATE = 0.25


def reconcile_behavioral_profile(
    belief: Belief,
    profile: dict,
) -> Belief:
    """
    Conservatively reconcile an aggregated behavioral profile
    with an existing belief.

    Behavioral evidence can reinforce an existing belief when
    there are repeated observations.

    A single observation is not enough to independently modify
    the belief because the original statement has already been
    processed by the normal knowledge pipeline.

    Behavioral evidence does not independently weaken a belief.
    Contradictions remain the responsibility of the existing
    belief reasoning system.
    """

    evidence_count = profile.get("evidence_count", 0)
    behavioral_confidence = profile.get("confidence", 0.0)

    if evidence_count < MIN_BEHAVIORAL_EVIDENCE:
        return belief

    if behavioral_confidence <= belief.confidence:
        return belief

    confidence_gap = (
        behavioral_confidence - belief.confidence
    )

    adjustment = (
        confidence_gap * REINFORCEMENT_RATE
    )

    belief.confidence = min(
        1.0,
        belief.confidence + adjustment,
    )

    return belief
