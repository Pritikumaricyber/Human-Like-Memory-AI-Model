from datetime import datetime

from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence


def update_belief(belief: Belief, evidence: Evidence) -> Belief:
    """
    Update a belief based on new evidence.

    This is the baseline rule-based updater.
    It is intentionally simple for now.

    Later, this will be replaced/improved
    with our research-based belief update algorithm.
    """

    evidence_strength = (
        evidence.reliability
        * evidence.specificity
        * evidence.independence
    )

    # -----------------------------------------
    # 1. SUPPORT
    # -----------------------------------------
    if evidence.relationship == "support":

        increase = evidence_strength * 0.20

        belief.confidence = min(
            1.0,
            belief.confidence + increase
        )

        if belief.confidence >= 0.70:
            belief.state = "supported"

    # -----------------------------------------
    # 2. CONTRADICTION
    # -----------------------------------------
    elif evidence.relationship == "contradict":

        decrease = evidence_strength * 0.20

        belief.confidence = max(
            0.0,
            belief.confidence - decrease
        )

        currentness_decrease = (
            evidence.reliability
            * evidence.specificity
            * 0.15
        )

        belief.currentness = max(
            0.0,
            belief.currentness - currentness_decrease
        )

        if belief.confidence < 0.40:
            belief.state = "weakened"

        elif belief.confidence < 0.60:
            belief.state = "contested"

        else:
            belief.state = "supported"

    # -----------------------------------------
    # 3. REFINEMENT
    # -----------------------------------------
    elif evidence.relationship == "refinement":

        # Refinement does not strongly increase
        # confidence. It makes the belief more specific.

        increase = evidence_strength * 0.05

        belief.confidence = min(
            1.0,
            belief.confidence + increase
        )

    # -----------------------------------------
    # 4. DUPLICATE
    # -----------------------------------------
    elif evidence.relationship == "duplicate":

        # Duplicate evidence should not artificially
        # strengthen the belief.

        pass

    # -----------------------------------------
    # 5. CONTEXT
    # -----------------------------------------
    elif evidence.relationship == "context":

        # Context provides useful information but
        # does not directly change belief confidence.

        pass

    # -----------------------------------------
    # 6. UNRELATED
    # -----------------------------------------
    elif evidence.relationship == "unrelated":

        # Completely unrelated evidence should have
        # no effect on the belief.

        pass

    # Update timestamp whenever the belief is processed
    belief.updated_at = datetime.now()

    return belief