from collections import deque

from backend.app.graph.belief_graph import BeliefGraph


def traverse_graph(
    graph: BeliefGraph,
    start_node: str,
    max_depth: int = 2
):
    """
    Traverse the belief graph using Breadth-First Search (BFS).

    Returns every connected node up to max_depth.
    """

    visited = set()

    queue = deque()

    queue.append((start_node, 0))

    connected = []

    while queue:

        node, depth = queue.popleft()

        if node in visited:
            continue

        visited.add(node)

        connected.append(node)

        if depth >= max_depth:
            continue

        for neighbor in graph.get_neighbors(node):

            if neighbor not in visited:
                queue.append(
                    (
                        neighbor,
                        depth + 1
                    )
                )

    return connected