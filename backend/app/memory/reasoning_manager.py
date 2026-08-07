from backend.app.models.belief import Belief
from backend.app.models.memory import Memory

from backend.app.memory.belief_reasoner import (
    reason_about_belief,
)


class ReasoningManager:
    """
    Manages belief reasoning and updates.
    """

    def process_reasoning(
        self,
        belief: Belief,
        memory: Memory,
    ) -> Belief:

        result = reason_about_belief(
            belief,
            memory,
        )

        belief.confidence = result["new_confidence"]
        belief.state = result["state"]

        print(
            f"Reasoning: {result['action']} "
            f"(confidence={belief.confidence:.2f}, "
            f"state={belief.state})"
        )

        return belief