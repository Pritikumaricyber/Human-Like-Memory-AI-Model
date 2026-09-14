from datetime import datetime, timedelta

from backend.app.models.memory import Memory

from backend.app.memory.forgetting_engine import (
    calculate_memory_retention,
    decide_forgetting,
)

from backend.app.memory.forgetting_manager import (
    ForgettingManager,
)


# =========================================================
# HELPER
# =========================================================

def print_memory_state(
    title: str,
    memory: Memory,
):
    retention = calculate_memory_retention(memory)
    decision = decide_forgetting(memory)

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("Content       :", memory.content)
    print("Importance    :", memory.importance)
    print("Emotion       :", memory.emotional_score)
    print("Confidence    :", memory.confidence)
    print("Recall Count  :", memory.recall_count)
    print("Strength      :", memory.strength)
    print("Age (days)    :", (datetime.now() - memory.created_at).days)
    print("Retention     :", round(retention, 3))
    print("Decision      :", decision)
    print("Status        :", memory.status)


# =========================================================
# CREATE FORGETTING MANAGER
# =========================================================

manager = ForgettingManager()


print("\n")
print("=" * 60)
print("HUMAN-LIKE FORGETTING CYCLE TEST")
print("=" * 60)


# =========================================================
# TEST 1 : FREQUENTLY RECALLED MEMORY
# =========================================================

frequent_memory = Memory(
    user_id="1",
    content="I frequently work on artificial intelligence projects.",
    memory_type="episodic",
    importance=0.8,
    emotional_score=0.7,
    confidence=0.9,
    strength=0.8,
    recall_count=10,
    created_at=datetime.now(),
    last_recalled=datetime.now(),
)

print_memory_state(
    "TEST 1 : FREQUENTLY RECALLED MEMORY - BEFORE",
    frequent_memory,
)

manager.process_memory(
    frequent_memory
)

print_memory_state(
    "TEST 1 : FREQUENTLY RECALLED MEMORY - AFTER",
    frequent_memory,
)


# =========================================================
# TEST 2 : NORMAL MEMORY
# =========================================================

normal_memory = Memory(
    user_id="1",
    content="I visited Ranchi during my semester break.",
    memory_type="episodic",
    importance=0.4,
    emotional_score=0.2,
    confidence=0.7,
    strength=0.5,
    recall_count=1,
    created_at=datetime.now() - timedelta(days=30),
    last_recalled=datetime.now() - timedelta(days=20),
)

print_memory_state(
    "TEST 2 : NORMAL MEMORY - BEFORE",
    normal_memory,
)

manager.process_memory(
    normal_memory
)

print_memory_state(
    "TEST 2 : NORMAL MEMORY - AFTER",
    normal_memory,
)


# =========================================================
# TEST 3 : OLD AND WEAK MEMORY
# =========================================================

weak_memory = Memory(
    user_id="1",
    content="I once visited an old restaurant.",
    memory_type="episodic",
    importance=0.1,
    emotional_score=0.0,
    confidence=0.3,
    strength=0.1,
    recall_count=0,
    created_at=datetime.now() - timedelta(days=180),
    last_recalled=datetime.now() - timedelta(days=180),
)

print_memory_state(
    "TEST 3 : OLD AND WEAK MEMORY - BEFORE",
    weak_memory,
)

manager.process_memory(
    weak_memory
)

print_memory_state(
    "TEST 3 : OLD AND WEAK MEMORY - AFTER",
    weak_memory,
)


# =========================================================
# TEST 4 : EMOTIONAL MEMORY
# =========================================================

emotional_memory = Memory(
    user_id="1",
    content="I achieved something very important to me.",
    memory_type="episodic",
    importance=0.6,
    emotional_score=0.95,
    confidence=0.9,
    strength=0.6,
    recall_count=0,
    created_at=datetime.now() - timedelta(days=120),
    last_recalled=datetime.now() - timedelta(days=100),
)

print_memory_state(
    "TEST 4 : EMOTIONAL MEMORY - BEFORE",
    emotional_memory,
)

manager.process_memory(
    emotional_memory
)

print_memory_state(
    "TEST 4 : EMOTIONAL MEMORY - AFTER",
    emotional_memory
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n")
print("=" * 60)
print("FINAL SUMMARY")
print("=" * 60)

memories = [
    ("Frequently recalled", frequent_memory),
    ("Normal memory", normal_memory),
    ("Old weak memory", weak_memory),
    ("Emotional memory", emotional_memory),
]

for name, memory in memories:

    retention = calculate_memory_retention(
        memory
    )

    decision = decide_forgetting(
        memory
    )

    print(
        f"{name:<25} "
        f"Retention={retention:.3f} | "
        f"Decision={decision:<9} | "
        f"Status={memory.status}"
    )

print("\nForgetting cycle test completed.")