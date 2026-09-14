from backend.app.models.memory import Memory

from backend.app.storage.belief_store import BeliefStore
from backend.app.storage.evidence_store import EvidenceStore
from backend.app.storage.history_store import HistoryStore

from backend.app.knowledge.knowledge_manager import (
    KnowledgeManager,
)


# ============================================================
# CREATE STORES
# ============================================================

belief_store = BeliefStore()
evidence_store = EvidenceStore()
history_store = HistoryStore()

manager = KnowledgeManager(
    belief_store=belief_store,
    evidence_store=evidence_store,
    history_store=history_store,
)


# ============================================================
# TEST 1 — STORE NEW BELIEF
# ============================================================

print("\n==============================")
print("KNOWLEDGE MANAGER")
print("==============================\n")

print("TEST 1: STORE NEW BELIEF")

memory = Memory(
    id="memory_001",
    user_id="user_001",
    content="User prefers Python.",
    memory_type="fact",
    importance=0.9,
    confidence=0.9,
    strength=0.8,
)

decision = {
    "action": "store_new",
    "target": None,
}

manager.process_knowledge(
    memory,
    decision,
)

print(
    "Beliefs:",
    belief_store.count(),
)


# ============================================================
# TEST 2 — STRENGTHEN EXISTING BELIEF
# ============================================================

print("\n------------------------------")
print("TEST 2: STRENGTHEN BELIEF")
print("------------------------------")

supporting_memory = Memory(
    id="memory_002",
    user_id="user_001",
    content="Python is my favorite language.",
    memory_type="fact",
    importance=0.9,
    confidence=0.9,
    strength=0.8,
)

decision = {
    "action": "strengthen_belief",
    "target": supporting_memory,
}

manager.process_knowledge(
    supporting_memory,
    decision,
)

print(
    "Beliefs:",
    belief_store.count(),
)

print(
    "Evidence:",
    evidence_store.count(),
)

print(
    "History:",
    history_store.count(),
)


# ============================================================
# TEST 3 — IGNORE DUPLICATE
# ============================================================

print("\n------------------------------")
print("TEST 3: IGNORE DUPLICATE")
print("------------------------------")

duplicate_memory = Memory(
    id="memory_003",
    user_id="user_001",
    content="User prefers Python.",
    memory_type="fact",
    importance=0.9,
    confidence=0.9,
    strength=0.8,
)

decision = {
    "action": "ignore",
    "target": duplicate_memory,
}

manager.process_knowledge(
    duplicate_memory,
    decision,
)

print(
    "Beliefs:",
    belief_store.count(),
)

print(
    "Evidence:",
    evidence_store.count(),
)

print(
    "History:",
    history_store.count(),
)


# ============================================================
# TEST 4 — CONTRADICT EXISTING BELIEF
# ============================================================

print("\n------------------------------")
print("TEST 4: CONTRADICT BELIEF")
print("------------------------------")

conflicting_memory = Memory(
    id="memory_004",
    user_id="user_001",
    content="I don't prefer Python anymore.",
    memory_type="fact",
    importance=0.9,
    confidence=0.9,
    strength=0.8,
)

decision = {
    "action": "revise_belief",
    "target": conflicting_memory,
}

manager.process_knowledge(
    conflicting_memory,
    decision,
)

print(
    "Beliefs:",
    belief_store.count(),
)

print(
    "Evidence:",
    evidence_store.count(),
)

print(
    "History:",
    history_store.count(),
)


# ============================================================
# FINAL STATE
# ============================================================

print("\n==============================")
print("FINAL KNOWLEDGE STATE")
print("==============================\n")

print(
    "Total beliefs:",
    belief_store.count(),
)

print(
    "Total evidence:",
    evidence_store.count(),
)

print(
    "Total history:",
    history_store.count(),
)

print("\nBELIEFS")

for belief in belief_store.get_all():

    print(
        f"Belief     : {belief.belief}"
    )

    print(
        f"Confidence : {belief.confidence:.2f}"
    )

    print(
        f"State      : {belief.state}"
    )

    print()