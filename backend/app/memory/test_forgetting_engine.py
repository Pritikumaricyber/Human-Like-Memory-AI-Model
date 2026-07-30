from datetime import datetime, timedelta

from backend.app.models.memory import Memory
from backend.app.memory.forgetting_engine import decide_forgetting


def run_test(title: str, memory: Memory):
    print("\n==============================")
    print(title)
    print("==============================")

    print("Content      :", memory.content)
    print("Importance   :", memory.importance)
    print("Strength     :", memory.strength)
    print("Recall Count :", memory.recall_count)
    print("Emotional    :", memory.emotional_score)

    age = (datetime.now() - memory.created_at).days
    print("Age (days)   :", age)

    decision = decide_forgetting(memory)

    print("\nDecision:", decision)


# KEEP
run_test(
    "KEEP MEMORY",
    Memory(
        user_id="user_001",
        content="I want to become an AI Engineer.",
        memory_type="goal",
        importance=0.9,
        confidence=0.9,
        strength=0.8,
        emotional_score=0.4,
        recall_count=2,
    ),
)

# ARCHIVE
run_test(
    "ARCHIVE MEMORY",
    Memory(
        user_id="user_001",
        content="I visited Ranchi.",
        memory_type="event",
        importance=0.4,
        confidence=0.9,
        strength=0.5,
        emotional_score=0.2,
        recall_count=2,
    ),
)

# FORGET
run_test(
    "FORGET MEMORY",
    Memory(
        user_id="user_001",
        content="Random weather information.",
        memory_type="fact",
        importance=0.2,
        confidence=0.8,
        strength=0.2,
        emotional_score=0.1,
        recall_count=0,
        created_at=datetime.now() - timedelta(days=120),
    ),
)