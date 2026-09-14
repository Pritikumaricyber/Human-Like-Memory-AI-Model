from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence

from backend.app.memory.belief_updater import (
    update_belief,
)


def update_behavioral_belief(
    belief: Belief,
    evidence: Evidence,
    reasoning_result: dict,
) -> Belief:
    """
    Apply a behavioral reasoning result to an
    existing belief using the existing belief updater.
    """

    return update_belief(
        belief=belief,
        evidence=evidence,
        new_confidence=reasoning_result.get(
            "new_confidence"
        ),
        new_state=reasoning_result.get(
            "state"
        ),
    )