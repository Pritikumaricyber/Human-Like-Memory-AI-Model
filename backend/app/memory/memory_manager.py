from backend.app.models.memory import Memory

from backend.app.memory.retrieval_engine import retrieve_memories
from backend.app.memory.consolidation_engine import consolidate_memory
from backend.app.memory.decision_engine import make_memory_decision
from backend.app.memory.reconsolidation_engine import reconsolidate_memory
from backend.app.memory.belief_builder import build_belief

from backend.app.storage.memory_store import MemoryStore
from backend.app.storage.belief_store import BeliefStore
from backend.app.storage.evidence_store import EvidenceStore
from backend.app.storage.history_store import HistoryStore

from backend.app.knowledge.knowledge_manager import KnowledgeManager


class MemoryManager:
    """
    Main controller of the Human-Like Memory system.
    """

    def __init__(self):

        self.memory_store = MemoryStore()
        self.belief_store = BeliefStore()
        self.evidence_store = EvidenceStore()
        self.history_store = HistoryStore()
        self.knowledge_manager = KnowledgeManager()

    def process_memory(
        self,
        new_memory: Memory
    ):

        # -----------------------------------------
        # Step 1 : Retrieve similar memories
        # -----------------------------------------

        retrieved = retrieve_memories(
            query=new_memory.content,
            memories=self.memory_store.get_all()
        )

        # -----------------------------------------
        # Step 2 : Consolidate
        # -----------------------------------------

        consolidation = consolidate_memory(
            new_memory,
            [item["memory"] for item in retrieved]
        )

        # -----------------------------------------
        # Step 3 : Decide
        # -----------------------------------------

        decision = make_memory_decision(
            consolidation
        )
        # -----------------------------------------
# Step 4 : Store Memory
# -----------------------------------------

        if decision["action"] == "store_new":
             self.memory_store.add(new_memory)

# -----------------------------------------
# Step 5 : Process Knowledge
# -----------------------------------------

        self.knowledge_manager.process_knowledge(
            new_memory,
            decision
)

        return {
            "retrieved": retrieved,
            "consolidation": consolidation,
            "decision": decision
        }