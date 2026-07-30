from backend.app.models.belief import Belief
from backend.app.storage.belief_store import BeliefStore


store = BeliefStore()

belief1 = Belief(
    id="b1",
    user_id="user_001",
    subject="Programming",
    belief="Python is my primary programming language.",
    confidence=0.90,
)

belief2 = Belief(
    id="b2",
    user_id="user_001",
    subject="Career",
    belief="AI is my career goal.",
    confidence=0.85,
)

print("\nADDING BELIEFS")
store.add(belief1)
store.add(belief2)

print("Count:", store.count())

print("\nALL BELIEFS")
for belief in store.get_all():
    print(belief.belief)

print("\nSEARCH")
found = store.get_by_id("b1")
print(found.belief if found else "Not Found")

print("\nDELETE")
store.delete("b2")
print("Count:", store.count())

print("\nCLEAR")
store.clear()
print("Count:", store.count())