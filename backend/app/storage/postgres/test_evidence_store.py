from backend.app.models.evidence import Evidence
from backend.app.storage.postgres.evidence_store import PostgresEvidenceStore


def test_evidence_store():

    store = PostgresEvidenceStore()

    # Start clean
    store.clear()

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    evidence = Evidence(
        user_id="test-user",
        belief_id="belief-123",
        content="I really enjoy using Python for AI work.",
        evidence_type="statement",
        relationship="support",
        reliability=0.9,
        specificity=0.95,
        independence=1.0,
    )

    store.add(evidence)

    print("ADD: PASS")

    # ---------------------------------------------------------
    # GET BY ID
    # ---------------------------------------------------------

    retrieved = store.get_by_id(evidence.id)

    assert retrieved is not None
    assert retrieved.id == evidence.id
    assert retrieved.user_id == evidence.user_id
    assert retrieved.belief_id == evidence.belief_id
    assert retrieved.content == evidence.content
    assert retrieved.relationship == "support"

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

    belief_records = store.find_by_belief("belief-123")

    assert len(belief_records) == 1
    assert belief_records[0].id == evidence.id

    print("FIND BY BELIEF: PASS")

    # ---------------------------------------------------------
    # FIND BY USER
    # ---------------------------------------------------------

    user_records = store.find_by_user("test-user")

    assert len(user_records) == 1
    assert user_records[0].id == evidence.id

    print("FIND BY USER: PASS")

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    evidence.reliability = 0.95
    evidence.independence = 0.8

    updated = store.update(evidence)

    assert updated is True

    retrieved = store.get_by_id(evidence.id)

    assert retrieved.reliability == 0.95
    assert retrieved.independence == 0.8

    print("UPDATE: PASS")

    # ---------------------------------------------------------
    # COUNT
    # ---------------------------------------------------------

    assert store.count() == 1

    print("COUNT: PASS")

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    deleted = store.delete(evidence.id)

    assert deleted is True
    assert store.count() == 0

    print("DELETE: PASS")

    print()
    print("PostgresEvidenceStore test completed successfully!")


if __name__ == "__main__":
    test_evidence_store()