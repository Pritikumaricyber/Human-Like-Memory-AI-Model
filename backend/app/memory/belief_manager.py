from backend.app.models.memory import Memory
from backend.app.models.belief import Belief


class BeliefManager:
    """
    Responsible for the complete lifecycle of beliefs.
    """

    def create_belief(
        self,
        memory: Memory
    ) -> Belief:
        """
        Create a belief from a semantic memory.
        """
        pass

    def strengthen_belief(
        self,
        belief: Belief,
        evidence
    ):
        """
        Strengthen an existing belief.
        """
        pass

    def revise_belief(
        self,
        belief: Belief,
        evidence
    ):
        """
        Revise a belief after contradiction.
        """
        pass

    def record_history(
        self,
        old_belief,
        new_belief,
        evidence
    ):
        """
        Store belief history.
        """
        pass