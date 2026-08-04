from backend.app.models.memory import Memory

from backend.app.memory.belief_builder import build_belief
from backend.app.memory.evidence_builder import build_evidence
from backend.app.memory.belief_updater import update_belief
from backend.app.memory.belief_history_manager import (
    record_belief_change,
)


class KnowledgeManager:
    """
    Manages the evolution of knowledge.

    Responsible for:
    - Creating beliefs
    - Updating beliefs
    - Creating evidence
    - Recording belief history
    """

    def __init__(
        self,
        belief_store,
        evidence_store,
        history_store,
    ):

        self.belief_store = belief_store
        self.evidence_store = evidence_store
        self.history_store = history_store

    def process_knowledge(
        self,
        memory: Memory,
        decision: dict,
    ) -> None:

        action = decision["action"]

        # -----------------------------------------
        # Store a completely new belief
        # -----------------------------------------

        if action == "store_new":

            belief = build_belief(memory)

            self.belief_store.add(belief)

            print("New belief created.")

            return

        # -----------------------------------------
        # Ignore duplicates
        # -----------------------------------------

        if action == "ignore":

            print("Duplicate belief ignored.")

            return

        # -----------------------------------------
        # Update an existing belief
        # -----------------------------------------

        if action not in (
            "strengthen_belief",
            "revise_belief",
        ):
            return

        target_memory = decision["target"]

        if target_memory is None:
            return

        belief = self.belief_store.find_by_subject(
            memory.content.split()[0]
        )

        if belief is None:

            belief = build_belief(memory)

            self.belief_store.add(belief)

        old_belief = belief.model_copy(deep=True)

        relationship = (
            "support"
            if action == "strengthen_belief"
            else "contradict"
        )

        evidence = build_evidence(
            memory,
            relationship,
        )

        self.evidence_store.add(evidence)

        updated_belief = update_belief(
            belief,
            evidence,
        )

        self.belief_store.update(updated_belief)

        history = record_belief_change(
            old_belief,
            updated_belief,
            evidence,
        )

        self.history_store.add(history)

        print("Belief updated.")

    def store_dream_beliefs(
        self,
        beliefs,
    ):
        """
        Store beliefs generated during the dream cycle.
        Avoid storing duplicate beliefs.
        """

        for belief in beliefs:

            existing = self.belief_store.find_by_subject(
                belief.subject
            )

            if existing is None:

                self.belief_store.add(belief)

                print(
                    f"Dream learned: {belief.belief}"
                )