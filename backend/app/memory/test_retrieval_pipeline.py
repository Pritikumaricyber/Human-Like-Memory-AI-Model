from backend.app.models.memory import Memory

from backend.app.storage.memory_store import MemoryStore

from backend.app.graph.belief_graph import BeliefGraph

from backend.app.memory.retrieval_pipeline import (
    run_retrieval_pipeline,
)


# -----------------------------
# Memory Store
# -----------------------------

memory_store = MemoryStore()

memories = [

    Memory(
        user_id="user_001",
        content="I use Python for AI.",
        memory_type="fact",
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
        memory_type="fact",
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
]

for memory in memories:
    memory_store.add(memory)


# -----------------------------
# Build Graph
# -----------------------------

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


# -----------------------------
# Retrieval Pipeline
# -----------------------------

retrieved = run_retrieval_pipeline(
    query="Python",
    memories=memory_store.get_all(),
    graph=graph,
)


print("\n==============================")
print("RETRIEVAL PIPELINE")
print("==============================\n")

for item in retrieved:

    print(item["memory"].content)
    print(
        "Score :",
        round(item["retrieval_score"], 4)
    )
    print()