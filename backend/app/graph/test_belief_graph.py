from backend.app.graph.belief_graph import BeliefGraph
from backend.app.graph.graph_traversal import traverse_graph

graph = BeliefGraph()

graph.add_relationship(
    "Python",
    "AI",
    "related",
    0.9
)

graph.add_relationship(
    "AI",
    "Machine Learning",
    "related",
    0.8
)

graph.add_relationship(
    "Machine Learning",
    "Deep Learning",
    "related",
    0.85
)

graph.add_relationship(
    "Python",
    "FastAPI",
    "used_for",
    0.95
)

print("\n==============================")
print("GRAPH TRAVERSAL")
print("==============================")

connected = traverse_graph(
    graph,
    "Python",
    max_depth=2
)

for node in connected:
    print(node)