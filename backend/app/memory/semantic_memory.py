class SemanticMemory:
    """
    Stores long-term factual knowledge.
    """

    def __init__(self):
        self.facts = []

    def add_fact(self, belief):
        """
        Store a learned fact.
        """
        self.facts.append(belief)

    def retrieve_all(self):
        """
        Return all stored facts.
        """
        return self.facts

    def size(self):
        return len(self.facts)

    def clear(self):
        self.facts.clear()