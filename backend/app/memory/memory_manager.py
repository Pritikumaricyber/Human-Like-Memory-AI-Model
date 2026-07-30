from backend.app.models.memory import Memory

from backend.app.memory.retrieval_engine import retrieve_memories
from backend.app.memory.consolidation_engine import consolidate_memory
from backend.app.memory.decision_engine import make_memory_decision
from backend.app.memory.belief_updater import update_belief
from backend.app.memory.reconsolidation_engine import reconsolidate_memory
from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence

class MemoryManager:

    def __init__(self):
        """
        Main controller of the Human-Like Memory system.
        """
        pass
       

    def process_memory(
        self,
        new_memory: Memory,
        stored_memories: list[Memory]
    ):

        # Step 1
        retrieved = retrieve_memories(
            query=new_memory.content,
            memories=stored_memories
        )

        # Step 2
        consolidation = consolidate_memory(
            new_memory,
            [item["memory"] for item in retrieved]
        )

        # Step 3
        decision = make_memory_decision(
            consolidation
        )

        # Step 4
        target = decision["target"]

        if target is not None:

            if decision["action"] in (
                "strengthen_belief",
                "revise_belief"
            ):
                print("Updating belief...") 
                print("Target memory:", target.content)

            elif decision["action"] == "update_memory":
                print("Reconsolidating memory...")

            elif decision["action"] == "ignore":
                print("Duplicate memory ignored.")

        else:
            print("Storing new memory...")

        return {
            "retrieved": retrieved,
            "consolidation": consolidation,
            "decision": decision
        }