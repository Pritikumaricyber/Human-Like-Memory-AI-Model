from collections import defaultdict


class BeliefGraph:
    """
    Graph storing relationships between beliefs.

    Nodes:
        Belief subjects

    Edges:
        Relationship between beliefs
    """

    def __init__(self):
        self.graph = defaultdict(list)

    def add_relationship(
        self,
        source: str,
        target: str,
        relationship: str,
        strength: float
    ) -> None:
        """
        Add a relationship between two beliefs.
        """

        self.graph[source].append(
            {
                "target": target,
                "relationship": relationship,
                "strength": strength
            }
        )

    def get_neighbors(
        self,
        node: str
    ) -> list[str]:
        """
        Return neighboring belief subjects.
        """

        return [
            edge["target"]
            for edge in self.graph.get(node, [])
        ]

    def get_relationships(
        self,
        node: str
    ) -> list[dict]:
        """
        Return complete relationship information.
        """

        return self.graph.get(node, [])

    def __len__(self):
        return len(self.graph)