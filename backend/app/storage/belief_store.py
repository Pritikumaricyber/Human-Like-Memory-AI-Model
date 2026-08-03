from backend.app.models.belief import Belief
from backend.app.storage.base_store import BaseStore


class BeliefStore(BaseStore[Belief]):
    """
    Stores and manages beliefs.
    """

    def find_by_subject(
        self,
        subject: str
    ) -> Belief | None:
        """
        Find a belief by its subject.
        """

        for belief in self.get_all():

            if belief.subject.lower() == subject.lower():
                return belief

        return None