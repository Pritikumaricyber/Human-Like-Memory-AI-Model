from backend.app.models.belief import Belief
from backend.app.models.memory import Memory

from backend.app.memory.belief_reasoner import (
    reason_about_belief,
)


def reason_about_behavioral_inference(
    belief: Belief,
    inference: dict,
) -> dict:
    """
    Pass a behavioral inference through the
    existing belief reasoning system.

    The existing reasoner operates on Memory objects,
    so the generated inference is represented as a
    temporary Memory for reasoning.
    """

    memory = Memory(
        user_id=belief.user_id,
        content=inference["inference"],
        memory_type="inference",
    )

    return reason_about_belief(
        belief=belief,
        memory=memory,
    )