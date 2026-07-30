from backend.app.models.belief_history import BeliefHistory
from backend.app.storage.history_store import HistoryStore


store = HistoryStore()

history1 = BeliefHistory(
    id="h1",
    belief_id="b1",
    evidence_id="e1",
    previous_confidence=0.60,
    new_confidence=0.80,
    previous_currentness=1.0,
    new_currentness=1.0,
    previous_state="new",
    new_state="supported",
    change_type="support",
)

history2 = BeliefHistory(
    id="h2",
    belief_id="b2",
    evidence_id="e2",
    previous_confidence=0.80,
    new_confidence=0.50,
    previous_currentness=1.0,
    new_currentness=0.90,
    previous_state="supported",
    new_state="contested",
    change_type="contradict",
)

print("\nADDING HISTORY")
store.add(history1)
store.add(history2)

print("Count:", store.count())

print("\nALL HISTORY")
for record in store.get_all():
    print(record.change_type)

print("\nSEARCH")
found = store.get_by_id("h1")
print(found.change_type if found else "Not Found")

print("\nDELETE")
store.delete("h2")
print("Count:", store.count())

print("\nCLEAR")
store.clear()
print("Count:", store.count())