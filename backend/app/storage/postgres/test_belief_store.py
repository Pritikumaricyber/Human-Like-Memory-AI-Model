from backend.app.models.belief import Belief
from backend.app.storage.postgres.belief_store import PostgresBeliefStore


def test_belief_store():

    store = PostgresBeliefStore()

    # Start clean
    store.clear()

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    belief = Belief(
        user_id="test-user",
        subject="Programming",
        belief="User prefers Python.",
        confidence=0.75,
        currentness=1.0,
        state="new",
    )

    store.add(belief)

    print("ADD: PASS")

    # ---------------------------------------------------------
    # GET BY ID
    # ---------------------------------------------------------

    retrieved = store.get_by_id(belief.id)

    assert retrieved is not None
    assert retrieved.id == belief.id
    assert retrieved.user_id == belief.user_id
    assert retrieved.subject == belief.subject
    assert retrieved.belief == belief.belief

    print("GET BY ID: PASS")

    # ---------------------------------------------------------
    # GET ALL
    # ---------------------------------------------------------

    beliefs = store.get_all()

    assert len(beliefs) == 1

    print("GET ALL: PASS")

    # ---------------------------------------------------------
    # FIND BY SUBJECT
    # ---------------------------------------------------------

    found = store.find_by_subject("programming")

    assert found is not None
    assert found.id == belief.id

    print("FIND BY SUBJECT: PASS")

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    belief.confidence = 0.95
    belief.state = "supported"

    updated = store.update(belief)

    assert updated is True

    retrieved = store.get_by_id(belief.id)

    assert retrieved.confidence == 0.95
    assert retrieved.state == "supported"

    print("UPDATE: PASS")

    # ---------------------------------------------------------
    # COUNT
    # ---------------------------------------------------------

    assert store.count() == 1

    print("COUNT: PASS")

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    deleted = store.delete(belief.id)

    assert deleted is True
    assert store.count() == 0

    print("DELETE: PASS")

    print()
    print("PostgresBeliefStore test completed successfully!")


if __name__ == "__main__":
    test_belief_store()