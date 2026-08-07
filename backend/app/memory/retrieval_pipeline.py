from backend.app.memory.retrieval_engine import retrieve_memories
from backend.app.graph.graph_retriever import retrieve_related_memories


def run_retrieval_pipeline(
    query,
    memories,
    graph,
):
    """
    Complete retrieval pipeline.

    Performs:
    1. Vector retrieval
    2. Graph retrieval
    3. Merge duplicate results
    """

    retrieved = retrieve_memories(
        query=query,
        memories=memories,
        emotion_store=None,
    )
    # Debug
    # print(f"Vector retrieval: {len(retrieved)}")

    graph_memories = retrieve_related_memories(
        graph=graph,
        memories=memories,
        start_subject=query,
        max_depth=2,
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
                    "retrieval_score": 0.60,
                }
            )

    retrieved.sort(
        key=lambda x: x["retrieval_score"],
        reverse=True,
    )

    return retrieved