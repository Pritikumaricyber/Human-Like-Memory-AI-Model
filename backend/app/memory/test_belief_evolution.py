from datetime import datetime, timedelta

from backend.app.models.belief_history import BeliefHistory

from backend.app.memory.belief_evolution import (
    analyze_belief_evolution,
)


now = datetime.now()


def create_history(
    previous_confidence: float,
    new_confidence: float,
    state: str,
    days_ago: int,
):
    return BeliefHistory(
        belief_id="belief_001",
        evidence_id=f"evidence_{days_ago}",
        previous_confidence=previous_confidence,
        new_confidence=new_confidence,
        previous_currentness=1.0,
        new_currentness=1.0,
        previous_state="supported",
        new_state=state,
        change_type=(
            "support"
            if new_confidence > previous_confidence
            else "contradict"
        ),
        created_at=now - timedelta(days=days_ago),
    )


# -----------------------------------------
# STRENGTHENING
# -----------------------------------------

strengthening_history = [

    create_history(
        0.50,
        0.65,
        "supported",
        3,
    ),

    create_history(
        0.65,
        0.80,
        "supported",
        2,
    ),

    create_history(
        0.80,
        0.90,
        "supported",
        1,
    ),
]


# -----------------------------------------
# DECLINING
# -----------------------------------------

declining_history = [

    create_history(
        0.90,
        0.75,
        "supported",
        3,
    ),

    create_history(
        0.75,
        0.55,
        "contested",
        2,
    ),

    create_history(
        0.55,
        0.30,
        "weakened",
        1,
    ),
]


# -----------------------------------------
# UNSTABLE
# -----------------------------------------

unstable_history = [

    create_history(
        0.50,
        0.70,
        "supported",
        3,
    ),

    create_history(
        0.70,
        0.45,
        "contested",
        2,
    ),

    create_history(
        0.45,
        0.65,
        "supported",
        1,
    ),
]


# -----------------------------------------
# STABLE
# -----------------------------------------

stable_history = [

    create_history(
        0.70,
        0.70,
        "supported",
        2,
    ),

    create_history(
        0.70,
        0.70,
        "supported",
        1,
    ),
]


# -----------------------------------------
# SUPERSEDED
# -----------------------------------------

superseded_history = [

    BeliefHistory(
        belief_id="belief_002",
        evidence_id="evidence_new",
        previous_confidence=0.40,
        new_confidence=0.20,
        previous_currentness=0.60,
        new_currentness=0.20,
        previous_state="contested",
        new_state="superseded",
        change_type="contradict",
        created_at=now,
    )
]


print("\n==============================")
print("BELIEF EVOLUTION")
print("==============================\n")


print(
    "Strengthening :",
    analyze_belief_evolution(
        strengthening_history
    ),
)

print(
    "Declining     :",
    analyze_belief_evolution(
        declining_history
    ),
)

print(
    "Unstable      :",
    analyze_belief_evolution(
        unstable_history
    ),
)

print(
    "Stable        :",
    analyze_belief_evolution(
        stable_history
    ),
)

print(
    "Superseded    :",
    analyze_belief_evolution(
        superseded_history
    ),
)
