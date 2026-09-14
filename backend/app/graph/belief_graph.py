from collections import defaultdict


class BeliefGraph:
    """
    Graph storing relationships between memories/beliefs.

    Nodes:
        Memory or belief subjects

    Edges:
        Relationships between nodes
    """

    def __init__(self):
        self.graph = defaultdict(list)

    def add_node(
        self,
        node: str,
    ) -> None:
        """
        Add a node to the graph if it does not already exist.
        """

        if node not in self.graph:
            self.graph[node] = []

    def add_relationship(
        self,
        source: str,
        target: str,
        relationship: str,
        strength: float,
    ) -> None:
        """
        Add a relationship between two nodes.
        """

        self.add_node(source)
        self.add_node(target)

        # Prevent duplicate relationships
        for edge in self.graph[source]:

            if (
                edge["target"] == target
                and edge["relationship"] == relationship
            ):
                return

        self.graph[source].append(
            {
                "target": target,
                "relationship": relationship,
                "strength": strength,
            }
        )

    def get_neighbors(
        self,
        node: str,
    ) -> list[str]:
        """
        Return neighboring nodes.
        """

        return [
            edge["target"]
            for edge in self.graph.get(node, [])
        ]

    def get_relationships(
        self,
        node: str,
    ) -> list[dict]:
        """
        Return complete relationship information.
        """

        return self.graph.get(node, [])

    def get_node_count(self) -> int:
        """
        Return number of graph nodes.
        """

        return len(self.graph)

    def get_relationship_count(self) -> int:
        """
        Return total number of relationships.
        """

        return sum(
            len(edges)
            for edges in self.graph.values()
        )

    def __len__(self):
        return len(self.graph)