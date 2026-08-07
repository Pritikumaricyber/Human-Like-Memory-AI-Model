from backend.app.models.belief import Belief
from backend.app.models.memory import Memory

from backend.app.memory.belief_conflict_detector import (
    detect_belief_conflict,
)
from backend.app.memory.confidence_calibrator import (
    calibrate_confidence,
)


def reason_about_belief(
    belief: Belief,
    memory: Memory,
) -> dict:
    """
    Decide how a belief should evolve after
    receiving new evidence.

    Supporting evidence:
        - increases confidence
        - marks belief as supported

    Contradicting evidence:
        - decreases confidence
        - marks belief as contested
    """

    conflict = detect_belief_conflict(
        belief,
        memory,
    )

    new_confidence = calibrate_confidence(
        belief.confidence,
        conflict,
    )

    if conflict:

        action = "weaken"
        state = "contested"

    else:

        action = "strengthen"
        state = "supported"

    return {
        "action": action,
        "conflict": conflict,
        "new_confidence": new_confidence,
        "state": state,
    }