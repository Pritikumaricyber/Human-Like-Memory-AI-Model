
from backend.app.memory.retrieval_engine import (
    calculate_retrieval_score,
    retrieve_memories,
    update_recall_state,
)
from backend.app.models.memory import Memory


# =========================================================
# TEST 1 : RETRIEVAL SCORE
# =========================================================

print("\n==============================")
print("TEST 1 : RETRIEVAL SCORE")
print("==============================")

memory = Memory(
    user_id="user_001",
    content="I am learning Python for AI.",
    memory_type="skill",
    importance=0.8,
    confidence=0.9,
    strength=0.7,
)

score = calculate_retrieval_score(
    semantic_similarity=0.9,
    memory=memory,
)

print("Memory:", memory.content)
print("Retrieval Score:", score)


# =========================================================
# TEST 2 : DORMANT MEMORY PENALTY
# =========================================================

print("\n==============================")
print("TEST 2 : DORMANT MEMORY")
print("==============================")

active_memory = Memory(
    user_id="user_001",
    content="Active memory",
    importance=0.8,
    confidence=0.9,
    strength=0.8,
    status="active",
)

dormant_memory = Memory(
    user_id="user_001",
    content="Dormant memory",
    importance=0.8,
    confidence=0.9,
    strength=0.8,
    status="dormant",
)

active_score = calculate_retrieval_score(
    semantic_similarity=0.8,
    memory=active_memory,
)

dormant_score = calculate_retrieval_score(
    semantic_similarity=0.8,
    memory=dormant_memory,
)

print("Active Score :", active_score)
print("Dormant Score:", dormant_score)

print(
    "Dormant penalty working:",
    dormant_score < active_score,
)


# =========================================================
# TEST 3 : FORGOTTEN MEMORY
# =========================================================

print("\n==============================")
print("TEST 3 : FORGOTTEN MEMORY")
print("==============================")

forgotten_memory = Memory(
    user_id="user_001",
    content="Forgotten memory",
    importance=0.8,
    confidence=0.9,
    strength=0.8,
    status="forgotten",
)

forgotten_score = calculate_retrieval_score(
    semantic_similarity=0.8,
    memory=forgotten_memory,
)

print("Forgotten Score:", forgotten_score)

print(
    "Forgotten score reduced:",
    forgotten_score < active_score,
)


# =========================================================
# TEST 4 : RECALL STATE UPDATE
# =========================================================

print("\n==============================")
print("TEST 4 : RECALL STATE")
print("==============================")

recall_memory = Memory(
    user_id="user_001",
    content="Dormant memory that gets recalled",
    importance=0.8,
    confidence=0.9,
    strength=0.5,
    status="dormant",
)

old_strength = recall_memory.strength
old_recall_count = recall_memory.recall_count

update_recall_state(
    recall_memory
)

print("Old Strength :", old_strength)
print("New Strength :", recall_memory.strength)

print(
    "Old Recall Count:",
    old_recall_count,
)

print(
    "New Recall Count:",
    recall_memory.recall_count,
)

print(
    "New Status:",
    recall_memory.status,
)

print(
    "Strength increased:",
    recall_memory.strength > old_strength,
)

print(
    "Recall count increased:",
    recall_memory.recall_count > old_recall_count,
)

print(
    "Dormant memory reactivated:",
    recall_memory.status == "active",
)


# =========================================================
# TEST 5 : ACTUAL MEMORY RETRIEVAL
# =========================================================

print("\n==============================")
print("TEST 5 : MEMORY RETRIEVAL")
print("==============================")

memories = [

    Memory(
        user_id="user_001",
        content="I use Python for AI.",
        memory_type="skill",
        importance=0.9,
        confidence=0.9,
        strength=0.9,
    ),

    Memory(
        user_id="user_001",
        content="I visited Ranchi yesterday.",
        memory_type="event",
        importance=0.5,
        confidence=0.9,
        strength=0.5,
    ),

    Memory(
        user_id="user_001",
        content="This memory has been forgotten.",
        memory_type="fact",
        importance=0.9,
        confidence=0.9,
        strength=0.9,
        status="forgotten",
    ),
]

retrieved = retrieve_memories(
    query="Python AI",
    memories=memories,
    top_k=5,
)


print("\nRetrieved Memories:")

for item in retrieved:

    memory = item["memory"]

    print(
        f"- {memory.content}"
        f" | similarity={item['semantic_similarity']}"
        f" | score={item['retrieval_score']}"
        f" | status={memory.status}"
    )


# =========================================================
# TEST 6 : FORGOTTEN MEMORY MUST NOT BE RETRIEVED
# =========================================================

print("\n==============================")
print("TEST 6 : FORGOTTEN EXCLUSION")
print("==============================")

forgotten_retrieved = any(
    item["memory"].status == "forgotten"
    for item in retrieved
)

print(
    "Forgotten memory retrieved:",
    forgotten_retrieved,
)

print(
    "Forgotten exclusion working:",
    not forgotten_retrieved,
)
