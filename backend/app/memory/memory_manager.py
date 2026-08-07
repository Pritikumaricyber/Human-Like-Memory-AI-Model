from backend.app.models.memory import Memory

from backend.app.memory.retrieval_engine import retrieve_memories
from backend.app.memory.consolidation_engine import consolidate_memory
from backend.app.memory.decision_engine import make_memory_decision
from backend.app.memory.reflection_engine import reflect

from backend.app.storage.memory_store import MemoryStore
from backend.app.storage.belief_store import BeliefStore
from backend.app.storage.evidence_store import EvidenceStore
from backend.app.storage.history_store import HistoryStore
from backend.app.storage.relationship_store import RelationshipStore

from backend.app.knowledge.knowledge_manager import KnowledgeManager

from backend.app.memory.relationship_engine import detect_relationship
from backend.app.memory.relationship_builder import build_relationship

from backend.app.graph.belief_graph import BeliefGraph
from backend.app.graph.graph_retriever import retrieve_related_memories

from backend.app.memory.dream_engine import run_dream_cycle

from backend.app.memory.reasoning_manager import (
    ReasoningManager,
)
from backend.app.memory.forgetting_manager import (
    ForgettingManager,
)
from backend.app.memory.emotion_detector import detect_emotion
from backend.app.memory.emotion_engine import apply_emotion
from backend.app.storage.emotion_store import EmotionStore


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
        self.emotion_store = EmotionStore()
        

        self.knowledge_manager = KnowledgeManager(
            belief_store=self.belief_store,
            evidence_store=self.evidence_store,
            history_store=self.history_store,
        )

        self.reasoning_manager = ReasoningManager()
        self.forgetting_manager = ForgettingManager()

    def process_memory(
        self,
        new_memory: Memory
    ):
        # -----------------------------------------
        # Emotion Detection
        # -----------------------------------------
        emotion = detect_emotion(
            user_id=new_memory.user_id,
            memory_id=new_memory.id,
            text=new_memory.content,
            )
        self.emotion_store.add(emotion)
        new_memory = apply_emotion(
            new_memory,
            emotion,
            )
        print(
            f"Emotion: {emotion.emotion}"
            )
        print(
            f"Intensity: {emotion.intensity}"
            )
        print(
            f"Valence: {emotion.valence}"
            )
        print(
            f"Arousal: {emotion.arousal}"
            )

        # -----------------------------------------
        # Step 1 : Retrieve similar memories
        # -----------------------------------------

        retrieved = retrieve_memories(
            query=new_memory.content,
            memories=self.memory_store.get_all(),
            emotion_store=self.emotion_store,
        )

        # -----------------------------------------
        # Graph Retrieval
        # -----------------------------------------

        from backend.app.memory.retrieval_pipeline import (
            run_retrieval_pipeline,
            )
        #print("Memory Count:", self.memory_store.count())
        #for m in self.memory_store.get_all():
            #print(">", m.content)
        retrieved = run_retrieval_pipeline(
            query=new_memory.content,
            memories=self.memory_store.get_all(),
            graph=self.graph,
            )
        #print("Retrieved:", len(retrieved))
        #print("Memory Count:", self.memory_store.count())
        #print("All memories:")
        #for m in self.memory_store.get_all():
            #print("-", m.content)
            #print("Retrieved:", len(retrieved))
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

        # -----------------------------------------
        # Step 5 : Build Relationships
        # -----------------------------------------

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
        # Step 7 : Reasoning
        # -----------------------------------------

        #print("Entering Reasoning Phase")

        for belief in self.belief_store.get_all():

            #print("Reasoning about:", belief.subject)

            self.reasoning_manager.process_reasoning(
                belief,
                new_memory
            )

        # -----------------------------------------
        # Step 8 : Reflection
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

        # -----------------------------------------
        # Step 9 : Dream Cycle
        # -----------------------------------------

        if self.memory_store.count() >= 5:

            dream_beliefs = run_dream_cycle(
                self.memory_store.get_all(),
                user_id=new_memory.user_id,
                emotion_store=self.emotion_store,
            )

            self.knowledge_manager.store_dream_beliefs(
                dream_beliefs
            )

            # Step 10 : Adaptive Forgetting
            for memory in self.memory_store.get_all():
                updated = self.forgetting_manager.process_memory(
                    memory
                    )
                DEBUG = True
                if DEBUG:
                    print(
                        f"Forgetting: {updated.content} -> {updated.status}"
                        )

        # -----------------------------------------
        # Return Pipeline Result
        # -----------------------------------------

        return {
            "retrieved": retrieved,
            "consolidation": consolidation,
            "decision": decision
        }