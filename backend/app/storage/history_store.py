from backend.app.models.belief_history import BeliefHistory
from backend.app.storage.base_store import BaseStore


class HistoryStore(BaseStore[BeliefHistory]):
    """
    Stores belief history.
    """
    pass