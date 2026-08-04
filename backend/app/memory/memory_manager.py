from backend.app.models.memory import Memory
from backend.app.memory.retrieval_engine import retrieve_memories
from backend.app.memory.consolidation_engine import consolidate_memory
from backend.app.memory.decision_engine import make_memory_decision
from backend.app.memory.reflection_engine import reflect
from backend.app.storage.memory_store import MemoryStore
from backend.app.storage.belief_store import BeliefStore
from backend.app.storage.evidence_store import EvidenceStore
from backend.app.storage.history_store import HistoryStore
from backend.app.knowledge.knowledge_manager import KnowledgeManager
from backend.app.storage.relationship_store import RelationshipStore
from backend.app.memory.relationship_engine import detect_relationship
from backend.app.memory.relationship_builder import build_relationship
from backend.app.graph.belief_graph import BeliefGraph
from backend.app.graph.graph_retriever import retrieve_related_memories
from backend.app.memory.dream_engine import run_dream_cycle

class MemoryManager:
    """
    Main controller of the Human-Like Memory system.
    """

    def __init__(self):

        self.memory_store = MemoryStore()
        self.belief_store = BeliefStore()
        self.evidence_store = EvidenceStore()
        self.history_store = HistoryStore()
        self.relationship_store = RelationshipStore()
        self.graph = BeliefGraph()

        self.knowledge_manager = KnowledgeManager(
            belief_store=self.belief_store,
            evidence_store=self.evidence_store,
            history_store=self.history_store,
        )
        

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
        # Graph Retrieval

        graph_memories = retrieve_related_memories(
            graph=self.graph,
            memories=self.memory_store.get_all(),
            start_subject=new_memory.content,
            max_depth=2
            )
        existing_ids = {
            item["memory"].id
            for item in retrieved
            }
        for memory in graph_memories:
            if memory.id not in existing_ids:
                retrieved.append(
                    {
                        "memory": memory,
                        "retrieval_score": 0.6
                        }
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

        self.memory_store.add(new_memory)
        

         # Step 5 : Build Relationships   

        for existing_memory in self.memory_store.get_all():
            if existing_memory.id == new_memory.id:
                continue
            relationship_type, strength = detect_relationship(
                new_memory,
                existing_memory
                )
            if relationship_type == "related":
                relationship = build_relationship(
                    new_memory,
                    existing_memory,
                    relationship_type,
                    strength
                    )
                self.relationship_store.add(relationship)
                self.graph.add_relationship(
                    new_memory.content,
                    existing_memory.content,
                    relationship_type,
                    strength
                    )
                print(
                    f"Relationship created "
                    f"({relationship_type}, {strength:.2f})"
                    )
    

        # -----------------------------------------
        # Step 6 : Process Knowledge
        # -----------------------------------------

        self.knowledge_manager.process_knowledge(
            new_memory,
            decision
        )

        # -----------------------------------------
        # Step 7 : Reflection
        # -----------------------------------------

        new_beliefs = reflect(
            self.memory_store.get_all()
        )

        for belief in new_beliefs:

            if self.belief_store.find_by_subject(
                belief.subject
            ) is None:

                self.belief_store.add(belief)

                print(
                    "Reflection learned:",
                    belief.belief
                )
                # Step 8 : Dream Cycle
               
                if self.memory_store.count() >= 5:
                    dream_beliefs = run_dream_cycle(
                        self.memory_store.get_all(),
                        user_id=new_memory.user_id
                        )
                    self.knowledge_manager.store_dream_beliefs(
                        dream_beliefs
                        )

        # -----------------------------------------
        # Return Pipeline Result
        # -----------------------------------------

        return {
            "retrieved": retrieved,
            "consolidation": consolidation,
            "decision": decision
        }