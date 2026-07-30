from typing import List

from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence
from backend.app.models.belief_history import BeliefHistory


def record_belief_change(
    old_belief: Belief,
    new_belief: Belief,
    evidence: Evidence
) -> BeliefHistory:
    """
    Create a history record describing how a belief changed.
    """

    return BeliefHistory(
        belief_id=old_belief.id or "unknown_belief",
        evidence_id=evidence.id or "unknown_evidence",

        previous_confidence=old_belief.confidence,
        new_confidence=new_belief.confidence,

        previous_currentness=old_belief.currentness,
        new_currentness=new_belief.currentness,

        previous_state=old_belief.state,
        new_state=new_belief.state,

        change_type=evidence.relationship
    )


def add_history(
    history: List[BeliefHistory],
    record: BeliefHistory
) -> List[BeliefHistory]:
    """
    Add a belief history record to the history list.
    """

    history.append(record)

    return history