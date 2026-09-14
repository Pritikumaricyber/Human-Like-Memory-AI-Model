from backend.app.memory.memory_manager import MemoryManager
from backend.app.memory.retrieval_pipeline import run_retrieval_pipeline


mm = MemoryManager()

memories = [
    m
    for m in mm.memory_store.get_all()
    if m.user_id == "user_001"
    and m.status != "forgotten"
]

results = run_retrieval_pipeline(
    query="What are my interests?",
    memories=memories,
    graph=mm.graph,
)

print("\n==============================")
print("RETRIEVAL SCORES")
print("==============================")

for i, result in enumerate(results, start=1):

    memory = result["memory"]

    print(
        f"{i}. "
        f"final={result['retrieval_score']:.4f} | "
        f"vector={result['vector_score']:.4f} | "
        f"graph={result['graph_score']:.4f} | "
        f"content={memory.content}"
    )