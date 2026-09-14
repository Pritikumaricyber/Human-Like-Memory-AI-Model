from backend.app.models.belief import Belief
from backend.app.storage.base_store import BaseStore


class BeliefStore(BaseStore[Belief]):
    """
    Stores and manages beliefs.
    """

    def find_by_subject(
        self,
        subject: str
    ) -> Belief | None:
        """
        Find a belief by its subject.
        """

        for belief in self.get_all():

            if belief.subject.lower() == subject.lower():
                return belief

        return None

    def find_similar_belief(
        self,
        belief_text: str,
        user_id: str,
        threshold: float = 0.70,
    ) -> tuple[Belief | None, float]:
        """
        Find the most semantically similar belief
        belonging to the same user.
        """

        from backend.app.memory.belief_matcher import (
            calculate_belief_similarity,
        )

        best_belief = None
        best_similarity = 0.0

        for belief in self.get_all():

            if belief.user_id != user_id:
                continue

            similarity = calculate_belief_similarity(
                belief_text,
                belief.belief,
            )

            if similarity > best_similarity:

                best_similarity = similarity
                best_belief = belief

        if best_similarity >= threshold:
            return best_belief, best_similarity

        return None, best_similarity