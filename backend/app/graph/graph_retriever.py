from backend.app.graph.belief_graph import BeliefGraph
from backend.app.graph.graph_traversal import traverse_graph
from backend.app.models.memory import Memory


def retrieve_related_memories(
    graph: BeliefGraph,
    memories: list[Memory],
    start_subject: str,
    max_depth: int = 2
) -> list[Memory]:
    """
    Retrieve memories connected through the belief graph.

    Example:
        Python
          ├── AI
          ├── FastAPI
          └── Machine Learning

    Asking about Python will also retrieve memories
    mentioning AI, FastAPI and Machine Learning.
    """

    connected_subjects = traverse_graph(
        graph,
        start_subject,
        max_depth
    )

    connected_subjects = {
        subject.lower()
        for subject in connected_subjects
    }

    related = []

    for memory in memories:

        text = memory.content.lower()

        for subject in connected_subjects:

            if subject in text:
                related.append(memory)
                break

    return related