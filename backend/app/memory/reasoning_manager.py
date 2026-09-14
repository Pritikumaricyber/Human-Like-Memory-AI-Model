from backend.app.models.belief import Belief
from backend.app.models.memory import Memory

from backend.app.memory.belief_reasoner import (
    reason_about_belief,
)


class ReasoningManager:
    """
    Manages reasoning about beliefs.

    The ReasoningManager determines how new evidence
    relates to an existing belief.

    It does NOT directly modify the belief.

    Belief state changes are handled by the
    KnowledgeManager and BeliefUpdater.
    """

    def process_reasoning(
        self,
        belief: Belief,
        memory: Memory,
    ) -> dict:
        """
        Reason about a belief using new memory.

        Returns the reasoning result without
        mutating the stored belief.
        """

        result = reason_about_belief(
            belief,
            memory,
        )

        print(
            f"Reasoning: {result['action']} "
            f"(confidence={result['new_confidence']:.2f}, "
            f"state={result['state']})"
        )

        return result