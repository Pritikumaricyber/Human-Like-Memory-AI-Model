from backend.app.memory.memory_manager import MemoryManager
from backend.app.graph.graph_retriever import retrieve_related_memories


mm = MemoryManager()

print("\n==============================")
print("GRAPH RETRIEVAL TEST")
print("==============================")

# ---------------------------------------------------------
# 1. Show graph structure
# ---------------------------------------------------------

print("\nGRAPH NODES:")

for node in mm.graph.graph:
    print(f"- {node}")

print("\nGRAPH EDGES:")

for source, edges in mm.graph.graph.items():

    for edge in edges:

        print(
            f"- {source} -> {edge['target']} | "
            f"relationship={edge['relationship']} | "
            f"strength={edge['strength']:.4f}"
        )

print(
    f"\nTotal nodes: "
    f"{mm.graph.get_node_count()}"
)

print(
    f"Total relationships: "
    f"{mm.graph.get_relationship_count()}"
)

# ---------------------------------------------------------
# 2. Get retrievable memories
# ---------------------------------------------------------

memories = [
    memory
    for memory in mm.memory_store.get_all()
    if (
        memory.user_id == "user_001"
        and memory.status != "forgotten"
    )
]

# ---------------------------------------------------------
# 3. Test graph retrieval
# ---------------------------------------------------------

query = "I use Python for AI."

print(f"\nQUERY: {query}")

results = retrieve_related_memories(
    graph=mm.graph,
    memories=memories,
    start_subject=query,
    max_depth=2,
)

# ---------------------------------------------------------
# 4. Display results
# ---------------------------------------------------------

print("\nGRAPH RETRIEVAL RESULTS:")

if not results:

    print("No graph results found.")

else:

    for index, item in enumerate(results, start=1):

        if isinstance(item, dict):

            memory = item.get("memory")

            strength = item.get(
                "relationship_strength",
                item.get("strength", 0.0),
            )

            print(
                f"{index}. "
                f"{memory.content if memory else 'None'} | "
                f"relationship={item.get('relationship')} | "
                f"strength={strength:.4f}"
            )

        else:

            print(
                f"{index}. {item.content}"
            )

# ---------------------------------------------------------
# 5. Final result
# ---------------------------------------------------------

print("\n==============================")

if results:

    print(
        "✅ GRAPH RETRIEVAL RETURNED RESULTS"
    )

else:

    print(
        "⚠️ GRAPH RETRIEVAL RETURNED NO RESULTS"
    )

print("==============================")