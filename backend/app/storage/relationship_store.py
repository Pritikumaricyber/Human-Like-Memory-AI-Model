from backend.app.models.relationship import Relationship
from backend.app.storage.base_store import BaseStore


class RelationshipStore(BaseStore[Relationship]):
    """
    Stores relationships between memories and beliefs.
    """

    def get_neighbors(
        self,
        node_id: str
    ) -> list[Relationship]:

        return [
            relation
            for relation in self.get_all()
            if relation.source_id == node_id
            or relation.target_id == node_id
        ]