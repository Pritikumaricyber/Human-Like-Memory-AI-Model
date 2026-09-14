from datetime import datetime, timedelta

from backend.app.models.memory import Memory

from backend.app.memory.memory_manager import MemoryManager
from backend.app.memory.retrieval_pipeline import (
    run_retrieval_pipeline,
)

from backend.app.memory.forgetting_engine import (
    calculate_memory_retention,
    decide_forgetting,
)


# =========================================================
# HELPERS
# =========================================================

def print_memory(memory: Memory):
    print(
        f"Content       : {memory.content}"
    )
    print(
        f"Type          : {memory.memory_type}"
    )
    print(
        f"Importance    : {memory.importance}"
    )
    print(
        f"Confidence    : {memory.confidence}"
    )
    print(
        f"Strength      : {memory.strength}"
    )
    print(
        f"Recall Count  : {memory.recall_count}"
    )
    print(
        f"Status        : {memory.status}"
    )


def separator(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# =========================================================
# CREATE MEMORY MANAGER
# =========================================================

manager = MemoryManager()


# =========================================================
# TEST 1 : CREATE INITIAL MEMORIES
# =========================================================

separator(
    "TEST 1 : CREATE INITIAL MEMORIES"
)


memories = [
    Memory(
        user_id="1",
        content="I use Python for AI projects.",
        memory_type="episodic",
        importance=0.8,
        confidence=0.9,
        strength=0.8,
    ),

    Memory(
        user_id="1",
        content="I enjoy building AI projects.",
        memory_type="episodic",
        importance=0.7,
        confidence=0.9,
        strength=0.7,
    ),

    Memory(
        user_id="1",
        content="FastAPI is useful for backend APIs.",
        memory_type="semantic",
        importance=0.6,
        confidence=0.9,
        strength=0.6,
    ),

    Memory(
        user_id="1",
        content="I visited Ranchi during my semester break.",
        memory_type="episodic",
        importance=0.4,
        confidence=0.7,
        strength=0.5,
    ),
]


print(
    f"Initial memories created: {len(memories)}"
)


# =========================================================
# STORE INITIAL MEMORIES
# =========================================================

for memory in memories:

    manager.memory_store.add(
        memory
    )


print(
    f"Stored memories: "
    f"{manager.memory_store.count()}"
)


# =========================================================
# TEST 2 : RETRIEVAL
# =========================================================

separator(
    "TEST 2 : MEMORY RETRIEVAL"
)


query = "I like working with Python and AI."

retrieved = run_retrieval_pipeline(
    query=query,
    memories=manager.memory_store.get_all(),
    graph=manager.graph,
)


print(
    f"Query: {query}"
)

print(
    f"\nRetrieved memories: {len(retrieved)}"
)


for item in retrieved:

    memory = item["memory"]

    print(
        f"\nMemory       : "
        f"{memory.content}"
    )

    print(
        f"Score        : "
        f"{item['retrieval_score']}"
    )

    print(
        f"Source       : "
        f"{item.get('retrieval_source', 'unknown')}"
    )

    print(
        f"Recall Count : "
        f"{memory.recall_count}"
    )

    print(
        f"Strength     : "
        f"{memory.strength}"
    )


# =========================================================
# TEST 3 : RELATIONSHIP GRAPH
# =========================================================

separator(
    "TEST 3 : RELATIONSHIP GRAPH"
)


manager.rebuild_memory_graph()

graph = manager.graph.graph


graph_nodes = len(graph)

graph_relationships = sum(
    len(neighbors)
    for neighbors in graph.values()
)


print(
    f"Graph nodes          : {graph_nodes}"
)

print(
    f"Graph relationships  : {graph_relationships}"
)


if graph_nodes > 0:

    print(
        "PASS: Relationship graph contains nodes."
    )

else:

    print(
        "WARNING: Relationship graph contains no nodes."
    )


if graph_relationships > 0:

    print(
        "PASS: Relationship graph contains relationships."
    )

else:

    print(
        "WARNING: Relationship graph contains no relationships."
    )


# =========================================================
# TEST 4 : CREATE NEW MEMORY THROUGH MEMORY MANAGER
# =========================================================

separator(
    "TEST 4 : PROCESS NEW MEMORY"
)


new_memory = Memory(
    user_id="1",
    content="Python is my favorite language for AI.",
    memory_type="episodic",
    importance=0.8,
    confidence=0.9,
    strength=0.7,
)


result = manager.process_memory(
    new_memory
)
# =====================================================
# PROCESS SECOND MEMORY TO UPDATE EXISTING BELIEF
# =====================================================

supporting_memory = Memory(
    user_id="1",
    content="I really enjoy using Python for my AI work.",
    memory_type="episodic",
    importance=0.8,
    confidence=0.9,
    strength=0.8,
)

manager.process_memory(
    supporting_memory
)


print(
    "\nMemoryManager returned:"
)

print(
    f"Retrieved results : "
    f"{len(result['retrieved'])}"
)

print(
    f"Consolidation     : "
    f"{len(result['consolidation'])}"
)

print(
    f"Decision           : "
    f"{result['decision']}"
)


# =========================================================
# TEST 5 : BELIEF FORMATION
# =========================================================

separator(
    "TEST 5 : BELIEF FORMATION"
)


beliefs = manager.belief_store.get_all()


print(
    f"Total beliefs: {len(beliefs)}"
)


for belief in beliefs:

    print(
        f"\nBelief       : "
        f"{belief.belief}"
    )

    print(
        f"Confidence   : "
        f"{belief.confidence}"
    )

    print(
        f"State        : "
        f"{belief.state}"
    )


if len(beliefs) > 0:

    print(
        "\nPASS: Belief system contains beliefs."
    )

else:

    print(
        "\nWARNING: No beliefs were created."
    )


# =========================================================
# TEST 6 : EVIDENCE
# =========================================================

separator(
    "TEST 6 : EVIDENCE SYSTEM"
)


evidence = manager.evidence_store.get_all()


print(
    f"Total evidence records: "
    f"{len(evidence)}"
)


for item in evidence:

    print(
        f"\nEvidence: "
        f"{item}"
    )


# =========================================================
# TEST 7 : HISTORY
# =========================================================

separator(
    "TEST 7 : BELIEF HISTORY"
)


history = manager.history_store.get_all()


print(
    f"Total history records: "
    f"{len(history)}"
)


for item in history:

    print(
        f"\nHistory: "
        f"{item}"
    )


# =========================================================
# TEST 8 : REFLECTION
# =========================================================

separator(
    "TEST 8 : REFLECTION"
)


print(
    "Reflection is executed automatically "
    "inside MemoryManager."
)

print(
    f"Beliefs after reflection: "
    f"{len(manager.belief_store.get_all())}"
)


# =========================================================
# TEST 9 : DREAM CYCLE
# =========================================================

separator(
    "TEST 9 : DREAM CYCLE"
)


print(
    "Dream cycle is executed automatically "
    "when enough memories exist."
)


print(
    f"Total beliefs after dream cycle: "
    f"{len(manager.belief_store.get_all())}"
)


# =========================================================
# TEST 10 : FORGETTING
# =========================================================

separator(
    "TEST 10 : FORGETTING"
)


for memory in manager.memory_store.get_all():

    retention = calculate_memory_retention(
        memory
    )

    decision = decide_forgetting(
        memory
    )

    print(
        f"\nMemory       : "
        f"{memory.content}"
    )

    print(
        f"Retention    : "
        f"{retention:.3f}"
    )

    print(
        f"Decision     : "
        f"{decision}"
    )

    print(
        f"Status       : "
        f"{memory.status}"
    )


# =========================================================
# TEST 11 : SIMULATE OLD MEMORY
# =========================================================

separator(
    "TEST 11 : OLD MEMORY SIMULATION"
)


old_memory = Memory(
    user_id="1",
    content="I once visited an old restaurant.",
    memory_type="episodic",
    importance=0.1,
    confidence=0.3,
    strength=0.1,
)


old_memory.created_at = (
    datetime.now() - timedelta(days=180)
)


manager.memory_store.add(
    old_memory
)


retention = calculate_memory_retention(
    old_memory
)

decision = decide_forgetting(
    old_memory
)


print_memory(
    old_memory
)

print(
    f"\nRetention    : "
    f"{retention:.3f}"
)

print(
    f"Decision     : "
    f"{decision}"
)


# =========================================================
# TEST 12 : APPLY FORGETTING
# =========================================================

separator(
    "TEST 12 : APPLY FORGETTING"
)


updated_old_memory = (
    manager.forgetting_manager.process_memory(
        old_memory
    )
)


print_memory(
    updated_old_memory
)


if updated_old_memory.status == "forgotten":

    print(
        "\nPASS: Old weak memory was forgotten."
    )

else:

    print(
        "\nWARNING: Old weak memory was not forgotten."
    )


# =========================================================
# TEST 13 : FORGOTTEN MEMORY RETRIEVAL
# =========================================================

separator(
    "TEST 13 : FORGOTTEN MEMORY RETRIEVAL"
)


retrieved_after_forgetting = (
    run_retrieval_pipeline(
        query="old restaurant",
        memories=manager.memory_store.get_all(),
        graph=manager.graph,
    )
)


forgotten_found = False


for item in retrieved_after_forgetting:

    memory = item["memory"]

    if memory.id == old_memory.id:

        forgotten_found = True

        print(
            "WARNING: Forgotten memory "
            "was retrieved."
        )


if not forgotten_found:

    print(
        "PASS: Forgotten memory "
        "was excluded from retrieval."
    )


# =========================================================
# FINAL SYSTEM SUMMARY
# =========================================================

separator(
    "FINAL SYSTEM SUMMARY"
)


print(
    f"Total memories       : "
    f"{manager.memory_store.count()}"
)

print(
    f"Total beliefs        : "
    f"{len(manager.belief_store.get_all())}"
)

print(
    f"Total evidence       : "
    f"{len(manager.evidence_store.get_all())}"
)

print(
    f"Total history        : "
    f"{len(manager.history_store.get_all())}"
)

print(
    f"Graph nodes          : "
     f"{len(manager.graph.graph)}"
)

total_graph_relationships = sum(
    len(neighbors)
    for neighbors in manager.graph.graph.values()
)

print(
    f"Graph relationships  : "
    f"{total_graph_relationships}"
)


# =========================================================
# MEMORY STATUS SUMMARY
# =========================================================

print(
    "\nMEMORY STATUS DISTRIBUTION"
)


active_count = 0
dormant_count = 0
forgotten_count = 0


for memory in manager.memory_store.get_all():

    if memory.status == "active":

        active_count += 1

    elif memory.status == "dormant":

        dormant_count += 1

    elif memory.status == "forgotten":

        forgotten_count += 1


print(
    f"Active     : {active_count}"
)

print(
    f"Dormant    : {dormant_count}"
)

print(
    f"Forgotten  : {forgotten_count}"
)


# =========================================================
# COMPLETION
# =========================================================

separator(
    "FULL MEMORY LIFECYCLE TEST COMPLETED"
)


print(
    "Human-like memory architecture "
    "integration test completed."
)