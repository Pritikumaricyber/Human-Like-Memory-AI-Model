from backend.app.models.memory import Memory

from backend.app.memory.retrieval_engine import (
    retrieve_memories,
)


print("\n" + "=" * 60)
print("RETRIEVAL + FORGETTING INTEGRATION TEST")
print("=" * 60)


# =========================================================
# TEST MEMORIES
# =========================================================

active_memory = Memory(
    user_id="1",
    content="I enjoy building AI projects.",
    memory_type="semantic",
    importance=0.8,
    confidence=0.9,
    strength=0.8,
    status="active",
)


dormant_memory = Memory(
    user_id="1",
    content="I visited Ranchi during my semester break.",
    memory_type="episodic",
    importance=0.4,
    confidence=0.7,
    strength=0.5,
    status="dormant",
)


forgotten_memory = Memory(
    user_id="1",
    content="I once visited an old restaurant.",
    memory_type="episodic",
    importance=0.1,
    confidence=0.3,
    strength=0.0,
    status="forgotten",
)


memories = [
    active_memory,
    dormant_memory,
    forgotten_memory,
]


# =========================================================
# BEFORE RETRIEVAL
# =========================================================

print("\n" + "=" * 60)
print("BEFORE RETRIEVAL")
print("=" * 60)

for memory in memories:

    print(
        f"\nContent      : {memory.content}"
    )

    print(
        f"Status       : {memory.status}"
    )

    print(
        f"Recall Count : {memory.recall_count}"
    )

    print(
        f"Strength     : {memory.strength}"
    )


# =========================================================
# RETRIEVAL
# =========================================================

print("\n" + "=" * 60)
print("RETRIEVING MEMORIES")
print("=" * 60)

query = "I enjoy working on AI projects."

retrieved = retrieve_memories(
    query=query,
    memories=memories,
    top_k=5,
)


# =========================================================
# RETRIEVED RESULTS
# =========================================================

print("\nRetrieved memories:")

for item in retrieved:

    memory = item["memory"]

    print(
        f"\nMemory       : {memory.content}"
    )

    print(
        f"Similarity   : "
        f"{item['semantic_similarity']}"
    )

    print(
        f"Score        : "
        f"{item['retrieval_score']}"
    )

    print(
        f"Status       : "
        f"{memory.status}"
    )

    print(
        f"Recall Count : "
        f"{memory.recall_count}"
    )

    print(
        f"Strength     : "
        f"{memory.strength}"
    )


# =========================================================
# VALIDATION
# =========================================================

print("\n" + "=" * 60)
print("VALIDATION")
print("=" * 60)


# ---------------------------------------------------------
# 1. Forgotten memory must NOT be retrieved
# ---------------------------------------------------------

forgotten_retrieved = any(
    item["memory"].id == forgotten_memory.id
    for item in retrieved
)


if forgotten_retrieved:

    print(
        "FAIL: Forgotten memory was retrieved."
    )

else:

    print(
        "PASS: Forgotten memory was excluded."
    )


# ---------------------------------------------------------
# 2. Active memory should be retrievable
# ---------------------------------------------------------

active_retrieved = any(
    item["memory"].id == active_memory.id
    for item in retrieved
)


if active_retrieved:

    print(
        "PASS: Active memory was retrieved."
    )

else:

    print(
        "WARNING: Active memory was not retrieved."
    )


# ---------------------------------------------------------
# 3. Check dormant memory behaviour
# ---------------------------------------------------------

dormant_retrieved = any(
    item["memory"].id == dormant_memory.id
    for item in retrieved
)


if dormant_retrieved:

    print(
        "PASS: Dormant memory remained retrievable."
    )

    print(
        f"Dormant memory status after retrieval: "
        f"{dormant_memory.status}"
    )

    print(
        f"Dormant memory recall count: "
        f"{dormant_memory.recall_count}"
    )

    print(
        f"Dormant memory strength: "
        f"{dormant_memory.strength}"
    )

else:

    print(
        "INFO: Dormant memory was not among the "
        "top retrieved memories for this query."
    )


# ---------------------------------------------------------
# 4. Validate recall strengthening
# ---------------------------------------------------------

if active_retrieved:

    if (
        active_memory.recall_count >= 1
        and active_memory.strength > 0.8
    ):

        print(
            "PASS: Retrieved memory was strengthened."
        )

    else:

        print(
            "FAIL: Retrieved memory was not strengthened."
        )


# =========================================================
# FINAL STATE
# =========================================================

print("\n" + "=" * 60)
print("FINAL MEMORY STATES")
print("=" * 60)

for memory in memories:

    print(
        f"\n{memory.content}"
    )

    print(
        f"Status       : {memory.status}"
    )

    print(
        f"Recall Count : {memory.recall_count}"
    )

    print(
        f"Strength     : {memory.strength}"
    )


print("\n" + "=" * 60)
print("RETRIEVAL + FORGETTING TEST COMPLETED")
print("=" * 60)