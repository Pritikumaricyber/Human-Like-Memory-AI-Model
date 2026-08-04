from backend.app.models.memory import Memory

from backend.app.memory.dream_engine import (
    run_dream_cycle,
)

memories = [

    Memory(
        user_id="1",
        content="I use Python.",
        strength=0.95,
        importance=0.90
    ),

    Memory(
        user_id="1",
        content="Python helps build AI systems.",
        strength=0.85,
        importance=0.80
    ),

    Memory(
        user_id="1",
        content="AI is my favorite field.",
        strength=0.82,
        importance=0.75
    ),

    Memory(
        user_id="1",
        content="FastAPI works with Python.",
        strength=0.70,
        importance=0.60
    )

]

beliefs = run_dream_cycle(memories)

print("\n==============================")
print("DREAM ENGINE")
print("==============================\n")

for belief in beliefs:

    print("Subject    :", belief.subject)
    print("Belief     :", belief.belief)
    print("Confidence :", belief.confidence)
    print()