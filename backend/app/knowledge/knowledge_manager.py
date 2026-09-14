from backend.app.models.memory import Memory
from backend.app.models.belief import Belief

from backend.app.memory.belief_builder import build_belief
from backend.app.memory.belief_matcher import (
    find_matching_belief,
)
from backend.app.memory.belief_reasoner import (
    reason_about_belief,
)

from backend.app.models.evidence import Evidence
from backend.app.models.belief_history import BeliefHistory


class KnowledgeManager:
    """
    Knowledge Manager

    Responsible for converting memories into knowledge by
    connecting:

        Memory
            ↓
        Belief Matching
            ↓
        Belief Reasoning
            ↓
        Evidence Creation
            ↓
        Belief Update
            ↓
        Belief History

    The manager uses the storage classes injected by
    MemoryManager.
    """

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(
        self,
        belief_store,
        evidence_store,
        history_store,
        belief_consolidator=None,
    ):
        """
        Initialize KnowledgeManager with persistent stores.
        """

        self.belief_store = belief_store
        self.evidence_store = evidence_store
        self.history_store = history_store
        self.belief_consolidator = belief_consolidator

    # =========================================================
    # PROCESS KNOWLEDGE
    # =========================================================

    def process_knowledge(
        self,
        memory: Memory,
        decision: dict | None = None,
    ):
        """
        Process a newly created memory.

        Pipeline:

            Memory
              ↓
            Find matching belief
              ↓
            If no match → create belief
              ↓
            If match → reason about evidence
              ↓
            Create evidence
              ↓
            Update belief
              ↓
            Record history
        """

        # -----------------------------------------------------
        # STEP 1
        # Find existing beliefs for this user
        # -----------------------------------------------------

        beliefs = [
            belief
            for belief in self.belief_store.get_all()
            if belief.user_id == memory.user_id
        ]

        # -----------------------------------------------------
        # STEP 2
        # Find matching belief
        # -----------------------------------------------------

        matching_belief, similarity = find_matching_belief(
            memory.content,
            beliefs,
        )

        # -----------------------------------------------------
        # STEP 3
        # No matching belief
        # -----------------------------------------------------

        if matching_belief is None:

            belief = build_belief(memory)

            self.belief_store.add(
                belief
            )

            print(
                f"New belief created: "
                f"{belief.belief}"
            )

            # -------------------------------------------------
            # Record origin evidence
            # -------------------------------------------------

            evidence = Evidence(
                user_id=memory.user_id,
                belief_id=belief.id,
                content=memory.content,
                evidence_type="statement",
                relationship="support",
                reliability=0.9,
                specificity=0.95,
                independence=1.0,
            )

            self.evidence_store.add(
                evidence
            )

            print(
                "Origin evidence recorded."
            )

            return {
                "action": "create_belief",
                "belief": belief,
                "evidence": evidence,
                "relationship": "support",
                "similarity": similarity,
            }

        # -----------------------------------------------------
        # STEP 4
        # Matching belief found
        # -----------------------------------------------------

        print(
            f"Matched belief: "
            f"{matching_belief.belief} "
            f"(similarity={similarity:.4f})"
        )

        # -----------------------------------------------------
        # STEP 5
        # Reason about new evidence
        # -----------------------------------------------------

        reasoning = reason_about_belief(
            matching_belief,
            memory,
        )

        print(
            f"Reasoning: "
            f"{reasoning['action']} "
            f"(confidence="
            f"{reasoning['new_confidence']:.2f}, "
            f"state="
            f"{reasoning['state']})"
        )

        # -----------------------------------------------------
        # STEP 6
        # Ignore unrelated evidence
        # -----------------------------------------------------

        if reasoning["action"] == "ignore":

            print(
                "Evidence ignored as unrelated."
            )

            return {
                "action": "ignore",
                "belief": matching_belief,
                "relationship": reasoning[
                    "relationship"
                ],
                "similarity": similarity,
            }

        # -----------------------------------------------------
        # STEP 7
        # Create evidence
        # -----------------------------------------------------

        evidence_relationship = reasoning[
            "relationship"
        ]

        evidence = Evidence(
            user_id=memory.user_id,
            belief_id=matching_belief.id,
            content=memory.content,
            evidence_type="statement",
            relationship=evidence_relationship,
            reliability=0.9,
            specificity=0.95,
            independence=self._calculate_independence(
                matching_belief,
                memory,
            ),
        )

        self.evidence_store.add(
            evidence
        )

        if evidence_relationship == "support":

            print(
                "Supporting evidence detected."
            )

        elif evidence_relationship == "contradict":

            print(
                "Contradicting evidence detected."
            )

        elif evidence_relationship == "refinement":

            print(
                "Refining evidence detected."
            )

        # -----------------------------------------------------
        # STEP 8
        # Save previous belief state
        # -----------------------------------------------------

        previous_confidence = (
            matching_belief.confidence
        )

        previous_currentness = (
            matching_belief.currentness
        )

        previous_state = (
            matching_belief.state
        )

        # -----------------------------------------------------
        # STEP 9
        # Update belief
        # -----------------------------------------------------

        matching_belief.confidence = (
            reasoning["new_confidence"]
        )

        matching_belief.state = (
            reasoning["state"]
        )

        matching_belief.currentness = (
            self._calculate_currentness(
                matching_belief,
                reasoning,
            )
        )

        # Update timestamp

        from datetime import datetime

        matching_belief.updated_at = (
            datetime.now()
        )

        # -----------------------------------------------------
        # STEP 10
        # Save updated belief
        # -----------------------------------------------------

        self._update_belief(
            matching_belief
        )

        # -----------------------------------------------------
        # STEP 11
        # Determine evolution type
        # -----------------------------------------------------

        evolution = self._determine_evolution(
            previous_confidence,
            matching_belief.confidence,
            previous_state,
            matching_belief.state,
            reasoning["relationship"],
        )

        print(
            f"Belief evolution: "
            f"{evolution}"
        )

        print(
            "Belief updated."
        )

        # -----------------------------------------------------
        # STEP 12
        # Record belief history
        # -----------------------------------------------------

        history = BeliefHistory(
            belief_id=matching_belief.id,
            evidence_id=evidence.id,
            previous_confidence=(
                previous_confidence
            ),
            new_confidence=(
                matching_belief.confidence
            ),
            previous_currentness=(
                previous_currentness
            ),
            new_currentness=(
                matching_belief.currentness
            ),
            previous_state=(
                previous_state
            ),
            new_state=(
                matching_belief.state
            ),
            change_type=(
                reasoning["relationship"]
            ),
        )

        self.history_store.add(
            history
        )

        # -----------------------------------------------------
        # RETURN RESULT
        # -----------------------------------------------------

        return {
            "action": reasoning["action"],
            "belief": matching_belief,
            "evidence": evidence,
            "history": history,
            "relationship": (
                reasoning["relationship"]
            ),
            "similarity": similarity,
            "evolution": evolution,
        }
    def find_existing_belief(
            self,
            belief: Belief,
            threshold: float = 0.70,
            ) -> tuple[Belief | None, float]:
        """
        Find the most semantically similar existing belief
        belonging to the same user.
        Returns:
           (existing_belief, similarity)
        If no belief reaches the threshold:
           (None, highest_similarity)
        """
        from backend.app.memory.belief_matcher import (
            calculate_belief_similarity,
            )
        existing_beliefs = [
            stored_belief
            for stored_belief in self.belief_store.get_all()
            if stored_belief.user_id == belief.user_id
            ]
        best_belief = None
        best_similarity = 0.0
        for stored_belief in existing_beliefs:
            similarity = calculate_belief_similarity(
                belief.belief,
                stored_belief.belief,
                )
            if similarity > best_similarity:
                best_similarity = similarity
                best_belief = stored_belief

    # IMPORTANT:
    # Only decide whether there is a match
    # after checking ALL existing beliefs.

        if (
            best_belief is not None
            and best_similarity >= threshold
            ):
            return best_belief, best_similarity
        return None, best_similarity
    # =========================================================
    # STORE DREAM BELIEFS
    # =========================================================

    def store_dream_beliefs(
        self,
        dream_beliefs: list[Belief],
    ):
        """
        Store beliefs generated by the dream cycle.

        Every dream-generated belief passes through the same
        semantic consolidation process so duplicate beliefs
        are not created.
        """

        for dream_belief in dream_beliefs:

            # -------------------------------------------------
            # Find semantically similar existing belief
            # -------------------------------------------------

            existing_belief, similarity = (
                self.find_existing_belief(
                    dream_belief,
                    threshold=0.70,
                )
            )

            # -------------------------------------------------
            # Existing belief found
            # -------------------------------------------------

            if existing_belief is not None:
                if existing_belief.state in {
                    "contested",
                    "superseded",
                }:
                    print(
                        f"Dream skipped reinforcement of "
                        f"{existing_belief.state} belief: "
                        f"{existing_belief.belief}"
                    )
                    continue

                print(
                    f"Dream reinforced existing belief: "
                    f"{existing_belief.belief} "
                    f"(matched: "
                    f"{dream_belief.belief}, "
                    f"similarity={similarity:.4f})"
                )

                # Reinforce currentness
                existing_belief.currentness = max(
                    existing_belief.currentness,
                    dream_belief.currentness,
                )

                # Keep stronger confidence
                existing_belief.confidence = max(
                    existing_belief.confidence,
                    dream_belief.confidence,
                )

                # Mark sufficiently strong beliefs as supported
                if existing_belief.confidence > 0.5:
                    existing_belief.state = "supported"

                # Update timestamp
                from datetime import datetime

                existing_belief.updated_at = datetime.now()

                # Save updated belief
                self._update_belief(
                    existing_belief
                )

                continue

            # -------------------------------------------------
            # Genuinely new belief
            # -------------------------------------------------

            self.belief_store.add(
                dream_belief
            )

            print(
                "Dream learned:",
                dream_belief.belief,
            )
        

    # =========================================================
    # UPDATE BELIEF
    # =========================================================

    def _update_belief(
        self,
        belief: Belief,
    ):
        """
        Update a belief inside the configured store.

        Supports stores that expose either:

            update(belief)

        or:

            add(belief)

        """

        # Preferred API

        if hasattr(
            self.belief_store,
            "update",
        ):

            self.belief_store.update(
                belief
            )

            return

        # Fallback

        if hasattr(
            self.belief_store,
            "add",
        ):

            self.belief_store.add(
                belief
            )

            return

        raise AttributeError(
            "BeliefStore must provide "
            "either update() or add()."
        )

    # =========================================================
    # INDEPENDENCE
    # =========================================================

    def _calculate_independence(
        self,
        belief: Belief,
        memory: Memory,
    ) -> float:
        """
        Estimate how independent the new evidence is.

        Currently uses a simple semantic-distance model.

        Higher independence means the evidence adds information
        that is not identical to previous belief wording.
        """

        from backend.app.memory.belief_matcher import (
            calculate_belief_similarity,
        )

        similarity = calculate_belief_similarity(
            memory.content,
            belief.belief,
        )

        independence = 1.0 - similarity

        # Keep a useful minimum.

        return max(
            0.10,
            min(
                1.0,
                independence,
            ),
        )

    # =========================================================
    # CURRENTNESS
    # =========================================================

    def _calculate_currentness(
        self,
        belief: Belief,
        reasoning: dict,
    ) -> float:
        """
        Update belief currentness based on evidence.

        Supporting evidence keeps a belief current.

        Contradicting evidence reduces currentness.

        Refinement slightly improves currentness.
        """

        relationship = reasoning[
            "relationship"
        ]

        currentness = belief.currentness

        if relationship == "support":

            currentness += 0.05

        elif relationship == "contradict":

            currentness -= 0.15

        elif relationship == "refinement":

            currentness += 0.02

        return max(
            0.0,
            min(
                1.0,
                currentness,
            ),
        )

    # =========================================================
    # DETERMINE EVOLUTION
    # =========================================================

    def _determine_evolution(
        self,
        previous_confidence: float,
        new_confidence: float,
        previous_state: str,
        new_state: str,
        relationship: str,
    ) -> str:
        """
        Determine how the belief evolved.
        """

        if relationship == "support":

            if new_confidence > previous_confidence:

                return "strengthening"

            return "stable"

        if relationship == "contradict":

            if new_confidence < previous_confidence:

                return "weakening"

            return "contested"

        if relationship == "refinement":

            return "refining"

        if new_state != previous_state:

            return (
                f"{previous_state}_to_"
                f"{new_state}"
            )

        return "stable"