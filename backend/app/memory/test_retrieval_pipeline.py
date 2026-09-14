
from backend.app.models.memory import Memory
from backend.app.storage.memory_store import MemoryStore
from backend.app.graph.belief_graph import BeliefGraph
from backend.app.memory.retrieval_pipeline import (
    run_retrieval_pipeline,
)


# =========================================================
# HELPER
# =========================================================

def print_results(title, retrieved):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    if not retrieved:
        print("No memories retrieved.")
        return

    for item in retrieved:
        memory = item["memory"]

        print(
            f"- {memory.content}"
            f" | score={item.get('retrieval_score', 0.0):.4f}"
            f" | semantic={item.get('semantic_similarity', 0.0):.4f}"
            f" | graph={item.get('graph_score', 0.0):.4f}"
            f" | relationship="
            f"{item.get('relationship_strength', 0.0):.4f}"
            f" | source={item.get('retrieval_source')}"
        )


# =========================================================
# TEST 1 : BASIC HYBRID RETRIEVAL
# =========================================================

print("\n==============================")
print("TEST 1 : BASIC HYBRID RETRIEVAL")
print("==============================")

memory_store = MemoryStore()

memories = [

    Memory(
        user_id="user_001",
        content="I use Python for AI.",
        memory_type="skill",
        importance=0.9,
        confidence=0.9,
        strength=0.9,
    ),

    Memory(
        user_id="user_001",
        content="FastAPI makes backend development easier.",
        memory_type="fact",
        importance=0.8,
        confidence=0.9,
        strength=0.8,
    ),

    Memory(
        user_id="user_001",
        content="Machine Learning is fascinating.",
        memory_type="skill",
        importance=0.8,
        confidence=0.9,
        strength=0.8,
    ),

    Memory(
        user_id="user_001",
        content="I visited Ranchi yesterday.",
        memory_type="event",
        importance=0.5,
        confidence=0.9,
        strength=0.5,
    ),

    Memory(
        user_id="user_001",
        content="This memory has been forgotten.",
        memory_type="fact",
        importance=0.9,
        confidence=0.9,
        strength=0.9,
        status="forgotten",
    ),
]

for memory in memories:
    memory_store.add(memory)


# ---------------------------------------------------------
# Build graph
# ---------------------------------------------------------

graph = BeliefGraph()

graph.add_relationship(
    "Python",
    "AI",
    "related",
    0.9,
)

graph.add_relationship(
    "Python",
    "FastAPI",
    "related",
    0.8,
)

graph.add_relationship(
    "AI",
    "Machine Learning",
    "related",
    0.9,
)


retrieved = run_retrieval_pipeline(
    query="Python",
    memories=memory_store.get_all(),
    graph=graph,
)

print_results(
    "BASIC RETRIEVAL RESULTS",
    retrieved,
)


# =========================================================
# CHECK 1 : RELEVANT MEMORY RETRIEVED
# =========================================================

python_found = any(
    item["memory"].content
    == "I use Python for AI."
    for item in retrieved
)

print(
    "\nRelevant Python memory retrieved:",
    python_found,
)


# =========================================================
# CHECK 2 : FORGOTTEN MEMORY EXCLUDED
# =========================================================

forgotten_found = any(
    item["memory"].status == "forgotten"
    for item in retrieved
)

print(
    "Forgotten memory retrieved:",
    forgotten_found,
)

print(
    "Forgotten exclusion working:",
    not forgotten_found,
)


# =========================================================
# CHECK 3 : IRRELEVANT RANCHI MEMORY EXCLUDED
# =========================================================

ranchi_found = any(
    item["memory"].content
    == "I visited Ranchi yesterday."
    for item in retrieved
)

print(
    "Irrelevant Ranchi memory retrieved:",
    ranchi_found,
)

print(
    "Irrelevant memory filtering working:",
    not ranchi_found,
)


# =========================================================
# TEST 2 : WEAK GRAPH RELATIONSHIP
# =========================================================

print("\n==============================")
print("TEST 2 : WEAK GRAPH RELATIONSHIP")
print("==============================")

weak_graph_memory = Memory(
    user_id="user_001",
    content="FastAPI is useful for backend APIs.",
    memory_type="fact",
    importance=0.8,
    confidence=0.9,
    strength=0.8,
)

weak_graph = BeliefGraph()

weak_graph.add_relationship(
    "Python",
    "FastAPI",
    "related",
    0.10,
)

weak_result = run_retrieval_pipeline(
    query="What am I learning?",
    memories=[weak_graph_memory],
    graph=weak_graph,
)

print_results(
    "WEAK GRAPH RESULTS",
    weak_result,
)

weak_graph_found = any(
    item["memory"].content
    == "FastAPI is useful for backend APIs."
    for item in weak_result
)

print(
    "\nWeak graph memory retrieved:",
    weak_graph_found,
)

print(
    "Weak graph filtering working:",
    not weak_graph_found,
)


# =========================================================
# TEST 3 : STRONG GRAPH EXCEPTION
# =========================================================

print("\n==============================")
print("TEST 3 : STRONG GRAPH EXCEPTION")
print("==============================")

strong_graph_memory = Memory(
    user_id="user_001",
    content="Neural networks are important to my AI work.",
    memory_type="skill",
    importance=0.9,
    confidence=0.9,
    strength=0.9,
)

strong_graph = BeliefGraph()

strong_graph.add_relationship(
    "AI",
    "Neural Networks",
    "related",
    0.95,
)

strong_result = run_retrieval_pipeline(
    query="AI",
    memories=[strong_graph_memory],
    graph=strong_graph,
)

print_results(
    "STRONG GRAPH RESULTS",
    strong_result,
)

strong_graph_found = any(
    item["memory"].content
    == "Neural networks are important to my AI work."
    for item in strong_result
)

print(
    "\nStrong graph memory retrieved:",
    strong_graph_found,
)

print(
    "Strong graph exception working:",
    strong_graph_found,
)


# =========================================================
# TEST 4 : DUPLICATE PREVENTION
# =========================================================

print("\n==============================")
print("TEST 4 : DUPLICATE PREVENTION")
print("==============================")

duplicate_memory = Memory(
    user_id="user_001",
    content="I enjoy building AI projects.",
    memory_type="fact",
    importance=0.9,
    confidence=0.9,
    strength=0.9,
)

duplicate_graph = BeliefGraph()

duplicate_graph.add_relationship(
    "AI",
    "AI Projects",
    "related",
    0.9,
)

duplicate_result = run_retrieval_pipeline(
    query="AI projects",
    memories=[duplicate_memory],
    graph=duplicate_graph,
)

print_results(
    "DUPLICATE TEST RESULTS",
    duplicate_result,
)

memory_ids = [
    item["memory"].id
    for item in duplicate_result
]

duplicates_exist = (
    len(memory_ids)
    != len(set(memory_ids))
)

print(
    "\nDuplicate memory returned:",
    duplicates_exist,
)

print(
    "Duplicate prevention working:",
    not duplicates_exist,
)


# =========================================================
# FINAL TEST SUMMARY
# =========================================================

print("\n==============================")
print("FINAL TEST SUMMARY")
print("==============================")

print(
    "Semantic retrieval:",
    "PASS" if python_found else "FAIL"
)

print(
    "Forgotten exclusion:",
    "PASS" if not forgotten_found else "FAIL"
)

print(
    "Irrelevant memory filtering:",
    "PASS" if not ranchi_found else "FAIL"
)

print(
    "Weak graph filtering:",
    "PASS" if not weak_graph_found else "FAIL"
)

print(
    "Strong graph exception:",
    "PASS" if strong_graph_found else "FAIL"
)

print(
    "Duplicate prevention:",
    "PASS" if not duplicates_exist else "FAIL"
)

