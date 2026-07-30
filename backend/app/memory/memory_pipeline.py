from copy import deepcopy

from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence

from backend.app.memory.belief_updater import update_belief
from backend.app.memory.belief_history_manager import record_belief_change


def process_evidence(
    belief: Belief,
    evidence: Evidence
):
    """
    Process new evidence against an existing belief.

    Returns:
        updated_belief
        history_record
    """

    # Keep a snapshot of the belief before modification
    old_belief = deepcopy(belief)

    # Update the actual belief
    updated_belief = update_belief(
        belief,
        evidence
    )

    # Record what changed
    history_record = record_belief_change(
        old_belief,
        updated_belief,
        evidence
    )

    return updated_belief, history_record