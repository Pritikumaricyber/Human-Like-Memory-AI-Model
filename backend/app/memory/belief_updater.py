from datetime import datetime

from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence


def update_belief(
    belief: Belief,
    evidence: Evidence,
    new_confidence: float | None = None,
    new_state: str | None = None,
) -> Belief:
    """
    Apply the result of belief reasoning to a belief.

    The reasoner decides how confidence and state should change.
    This function applies that decision to the actual belief.
    """

    # -------------------------------------------------
    # Use reasoning result when provided
    # -------------------------------------------------

    if new_confidence is not None:

        belief.confidence = max(
            0.0,
            min(1.0, new_confidence)
        )

    # -------------------------------------------------
    # Apply new belief state
    # -------------------------------------------------

    if new_state is not None:

        belief.state = new_state

    # -------------------------------------------------
    # Update currentness when evidence contradicts
    # -------------------------------------------------

    if evidence.relationship == "contradict":

        currentness_decrease = (
            evidence.reliability
            * evidence.specificity
            * 0.15
        )

        belief.currentness = max(
            0.0,
            belief.currentness - currentness_decrease
        )

    # -------------------------------------------------
    # Update timestamp
    # -------------------------------------------------

    belief.updated_at = datetime.now()

    return belief