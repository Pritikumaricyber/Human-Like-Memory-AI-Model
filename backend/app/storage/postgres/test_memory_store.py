from backend.app.models.memory import Memory
from backend.app.storage.postgres.memory_store import PostgresMemoryStore


def test_memory_store():

    store = PostgresMemoryStore()

    # Start clean
    store.clear()

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    memory = Memory(
        user_id="test-user",
        content="I am testing PostgreSQL memory storage.",
        memory_type="fact",
        importance=0.8,
        emotional_score=0.4,
        confidence=0.9,
        frequency=2,
        strength=0.85,
        decay_rate=0.01,
        topics=["testing", "postgresql"],
        entities=["PostgreSQL"],
        related_memories=[],
        status="active",
        recall_count=3,
    )

    store.add(memory)

    print("ADD: PASS")

    # ---------------------------------------------------------
    # GET BY ID
    # ---------------------------------------------------------

    retrieved = store.get_by_id(memory.id)

    assert retrieved is not None
    assert retrieved.id == memory.id
    assert retrieved.content == memory.content
    assert retrieved.user_id == memory.user_id
    assert retrieved.topics == memory.topics
    assert retrieved.recall_count == memory.recall_count

    print("GET BY ID: PASS")

    # ---------------------------------------------------------
    # GET ALL
    # ---------------------------------------------------------

    memories = store.get_all()

    assert len(memories) == 1

    print("GET ALL: PASS")

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    memory.strength = 0.95
    memory.recall_count = 5

    updated = store.update(memory)

    assert updated is True

    retrieved = store.get_by_id(memory.id)

    assert retrieved.strength == 0.95
    assert retrieved.recall_count == 5

    print("UPDATE: PASS")

    # ---------------------------------------------------------
    # COUNT
    # ---------------------------------------------------------

    assert store.count() == 1

    print("COUNT: PASS")

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    deleted = store.delete(memory.id)

    assert deleted is True
    assert store.count() == 0

    print("DELETE: PASS")

    print()
    print("PostgresMemoryStore test completed successfully!")


if __name__ == "__main__":
    test_memory_store()