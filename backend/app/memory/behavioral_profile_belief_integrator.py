from backend.app.models.belief import Belief

from backend.app.memory.behavioral_confidence_belief_integrator import (
    apply_behavioral_confidence
)


def integrate_behavioral_profile(
    belief: Belief,
    profile: dict,
) -> Belief:
    """
    Apply a consolidated behavioral profile to an existing belief.
    """

    confidence = profile.get("confidence", 0.0)

    return apply_behavioral_confidence(
        belief,
        confidence,
    )