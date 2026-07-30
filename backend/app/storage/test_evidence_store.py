from backend.app.models.evidence import Evidence
from backend.app.storage.evidence_store import EvidenceStore


store = EvidenceStore()

evidence1 = Evidence(
    id="e1",
    user_id="user_001",
    content="User said Python is their favorite language.",
    evidence_type="statement",
    relationship="support",
    reliability=0.95,
)

evidence2 = Evidence(
    id="e2",
    user_id="user_001",
    content="User started learning Java.",
    evidence_type="behavior",
    relationship="refinement",
    reliability=0.80,
)

print("\nADDING EVIDENCE")
store.add(evidence1)
store.add(evidence2)

print("Count:", store.count())

print("\nALL EVIDENCE")
for evidence in store.get_all():
    print(evidence.content)

print("\nSEARCH")
found = store.get_by_id("e1")
print(found.content if found else "Not Found")

print("\nDELETE")
store.delete("e2")
print("Count:", store.count())

print("\nCLEAR")
store.clear()
print("Count:", store.count())