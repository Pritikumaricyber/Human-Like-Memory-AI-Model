from backend.app.models.belief import Belief


belief = Belief(
    user_id="user_001",
    subject="user_001",
    belief="User prefers Python",
    confidence=0.90,
    currentness=0.85,
    state="supported"
)

print(belief.model_dump())