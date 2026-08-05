from backend.app.models.memory import Memory

from backend.app.memory.semantic_learning_pipeline import (
    run_semantic_learning,
)

memories = [

    Memory(
        user_id="user_001",
        content="Python is great",
        memory_type="fact",
        strength=0.9,
        importance=0.9,
    ),

    Memory(
        user_id="user_001",
        content="Python is useful",
        memory_type="fact",
        strength=0.8,
        importance=0.8,
    ),

    Memory(
        user_id="user_001",
        content="I build FastAPI APIs",
        memory_type="fact",
        strength=0.8,
        importance=0.8,
    ),

    Memory(
        user_id="user_001",
        content="AI is fascinating",
        memory_type="fact",
        strength=0.9,
        importance=0.8,
    ),
]

beliefs = run_semantic_learning(
    memories,
    user_id="user_001",
)

print("\n==============================")
print("SEMANTIC LEARNING PIPELINE")
print("==============================\n")

for belief in beliefs:

    print("Subject    :", belief.subject)
    print("Belief     :", belief.belief)
    print("Confidence :", belief.confidence)
    print()