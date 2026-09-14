from backend.app.models.belief import Belief


class BeliefConsolidator:
    """
    Consolidates semantically duplicate beliefs.

    Instead of creating multiple beliefs that express
    essentially the same knowledge, the consolidator
    merges new information into an existing belief.
    """

    def __init__(
        self,
        belief_store,
        similarity_threshold: float = 0.70,
    ):
        self.belief_store = belief_store
        self.similarity_threshold = similarity_threshold

    def consolidate(
        self,
        belief: Belief,
    ) -> dict:
        """
        Check whether a belief already exists.

        Returns:

            {
                "action": "merged" | "created",
                "belief": Belief,
                "similarity": float
            }
        """

        existing_belief, similarity = (
            self.belief_store.find_similar_belief(
                belief.belief,
                belief.user_id,
                threshold=self.similarity_threshold,
            )
        )

        # -------------------------------------------------
        # No similar belief
        # -------------------------------------------------

        if existing_belief is None:

            self.belief_store.add(
                belief
            )

            return {
                "action": "created",
                "belief": belief,
                "similarity": similarity,
            }

        # -------------------------------------------------
        # Similar belief already exists
        # -------------------------------------------------

        previous_confidence = (
            existing_belief.confidence
        )

        # Keep the stronger confidence.

        existing_belief.confidence = max(
            existing_belief.confidence,
            belief.confidence,
        )

        # A newly generated belief can reinforce
        # an existing belief.

        if existing_belief.confidence > 0.5:

            existing_belief.state = "supported"

        # Refresh currentness.

        existing_belief.currentness = max(
            existing_belief.currentness,
            belief.currentness,
        )

        # Update timestamp.

        from datetime import datetime

        existing_belief.updated_at = (
            datetime.now()
        )

        # Save.

        if hasattr(
            self.belief_store,
            "update",
        ):

            self.belief_store.update(
                existing_belief
            )

        else:

            self.belief_store.add(
                existing_belief
            )

        return {
            "action": "merged",
            "belief": existing_belief,
            "similarity": similarity,
            "previous_confidence": previous_confidence,
            "new_confidence": (
                existing_belief.confidence
            ),
        }