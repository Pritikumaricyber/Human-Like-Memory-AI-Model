from backend.app.models.belief_history import BeliefHistory
from backend.app.storage.postgres.history_store import PostgresHistoryStore


def test_history_store():

    store = PostgresHistoryStore()

    # Start clean
    store.clear()

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    history = BeliefHistory(
        belief_id="belief-123",
        evidence_id="evidence-123",
        previous_confidence=0.70,
        new_confidence=0.85,
        previous_currentness=0.90,
        new_currentness=1.0,
        previous_state="new",
        new_state="supported",
        change_type="support",
    )

    store.add(history)

    print("ADD: PASS")

    # ---------------------------------------------------------
    # GET BY ID
    # ---------------------------------------------------------

    retrieved = store.get_by_id(history.id)

    assert retrieved is not None
    assert retrieved.id == history.id
    assert retrieved.belief_id == "belief-123"
    assert retrieved.evidence_id == "evidence-123"
    assert retrieved.new_confidence == 0.85
    assert retrieved.new_state == "supported"

    print("GET BY ID: PASS")

    # ---------------------------------------------------------
    # GET ALL
    # ---------------------------------------------------------

    records = store.get_all()

    assert len(records) == 1

    print("GET ALL: PASS")

    # ---------------------------------------------------------
    # FIND BY BELIEF
    # ---------------------------------------------------------

    belief_history = store.find_by_belief("belief-123")

    assert len(belief_history) == 1
    assert belief_history[0].id == history.id

    print("FIND BY BELIEF: PASS")

    # ---------------------------------------------------------
    # COUNT
    # ---------------------------------------------------------

    assert store.count() == 1

    print("COUNT: PASS")

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    deleted = store.delete(history.id)

    assert deleted is True
    assert store.count() == 0

    print("DELETE: PASS")

    print()
    print("PostgresHistoryStore test completed successfully!")


if __name__ == "__main__":
    test_history_store()