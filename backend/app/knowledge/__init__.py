class KnowledgeManager:
    """
    Manages the evolution of knowledge.
    """

    def __init__(
        self,
        belief_store,
        evidence_store,
        history_store
    ):
        self.belief_store = belief_store
        self.evidence_store = evidence_store
        self.history_store = history_store