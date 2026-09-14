from backend.app.models.memory import Memory
from backend.app.memory.memory_manager import MemoryManager


# =========================================================
# BEHAVIORAL CONTRADICTION E2E TEST
# =========================================================

USER_ID = "behavioral_contradiction_e2e_test"


def separator(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


manager = MemoryManager()


# =========================================================
# TEST 1 : POSITIVE BEHAVIORAL OBSERVATIONS
# =========================================================

separator("TEST 1 : POSITIVE BEHAVIORAL OBSERVATIONS")


positive_memories = [
    "I prefer Python.",
    "I love Python.",
    "I enjoy using Python.",
]


for text in positive_memories:

    print(f"\nProcessing: {text}")

    memory = Memory(
        user_id=USER_ID,
        content=text,
        memory_type="episodic",
        importance=0.8,
        confidence=0.9,
        strength=0.8,
    )

    manager.process_memory(memory)


# =========================================================
# TEST 2 : CHECK BELIEF BEFORE CONTRADICTION
# =========================================================

separator("TEST 2 : BELIEF BEFORE CONTRADICTION")


beliefs = [
    belief
    for belief in manager.belief_store.get_all()
    if belief.user_id == USER_ID
]


for belief in beliefs:

    print(
        f"Belief     : {belief.belief}"
    )

    print(
        f"Confidence : {belief.confidence:.4f}"
    )

    print(
        f"State      : {belief.state}"
    )


# =========================================================
# TEST 3 : CONTRADICTING OBSERVATION
# =========================================================

separator("TEST 3 : CONTRADICTING OBSERVATION")


contradiction = Memory(
    user_id=USER_ID,
    content="I do not like Python anymore.",
    memory_type="episodic",
    importance=0.9,
    confidence=0.9,
    strength=0.9,
)


manager.process_memory(contradiction)


# =========================================================
# TEST 4 : FINAL BELIEF STATE
# =========================================================

separator("TEST 4 : FINAL BELIEF STATE")


final_beliefs = [
    belief
    for belief in manager.belief_store.get_all()
    if belief.user_id == USER_ID
]


for belief in final_beliefs:

    print(
        f"\nBelief     : {belief.belief}"
    )

    print(
        f"Confidence : {belief.confidence:.4f}"
    )

    print(
        f"State      : {belief.state}"
    )


# =========================================================
# TEST 5 : CONTRADICTION PROTECTION
# =========================================================

separator("TEST 5 : CONTRADICTION PROTECTION")


contested_beliefs = [
    belief
    for belief in final_beliefs
    if belief.state == "contested"
]


if contested_beliefs:

    print(
        "PASS: Contradicting evidence produced "
        "a contested belief."
    )

else:

    print(
        "FAIL: No contested belief was produced."
    )


supported_after_contradiction = [
    belief
    for belief in final_beliefs
    if (
        belief.state == "supported"
        and "Python" in belief.belief
    )
]


if supported_after_contradiction:

    print(
        "FAIL: Reflection/Dream appears to have "
        "resurrected the contradicted Python belief."
    )

else:

    print(
        "PASS: Contradicted Python belief was not "
        "resurrected as supported."
    )


separator("BEHAVIORAL CONTRADICTION E2E TEST COMPLETED")