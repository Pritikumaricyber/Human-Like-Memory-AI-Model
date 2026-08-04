from backend.app.memory.insight_builder import (
    build_insights,
)

patterns = {
    "python": 4,
    "ai": 3,
    "fastapi": 1
}

beliefs = build_insights(
    patterns,
    user_id="1"
)

print("\n==============================")
print("INSIGHT BUILDER")
print("==============================\n")

for belief in beliefs:

    print("Subject    :", belief.subject)
    print("Belief     :", belief.belief)
    print("Confidence :", belief.confidence)
    print("State      :", belief.state)
    print()