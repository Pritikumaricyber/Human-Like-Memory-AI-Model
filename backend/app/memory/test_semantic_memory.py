from backend.app.memory.semantic_memory import SemanticMemory
from backend.app.models.belief import Belief

semantic = SemanticMemory()

semantic.add_fact(

    Belief(
        user_id="user_001",
        subject="user_001",
        belief="User prefers Python for AI.",
        confidence=0.95,
        currentness=1.0,
        state="supported"
    )
)

semantic.add_fact(

    Belief(
        user_id="user_001",
        subject="user_001",
        belief="User wants to become an AI Engineer.",
        confidence=0.90,
        currentness=1.0,
        state="supported"
    )
)

print("\nSEMANTIC MEMORY\n")

for belief in semantic.retrieve_all():

    print("------------------------")
    print("Fact       :", belief.belief)
    print("Confidence :", belief.confidence)
    print("State      :", belief.state)

print("\nTotal Facts:", semantic.size())