from backend.app.storage.memory_store import MemoryStore
from backend.app.models.memory import Memory


store = MemoryStore()

memory1 = Memory(
    id="m1",
    user_id="user1",
    content="I use Python.",
    memory_type="fact"
)

memory2 = Memory(
    id="m2",
    user_id="user1",
    content="I visited Ranchi.",
    memory_type="event"
)

print("\nADDING MEMORIES")
store.add(memory1)
store.add(memory2)

print("Count:", store.count())

print("\nALL MEMORIES")
for memory in store.get_all():
    print(memory.content)

print("\nSEARCH BY ID")
found = store.get_by_id("m1")
print(found.content if found else "Not Found")

print("\nDELETE MEMORY")
store.delete("m2")
print("Count:", store.count())

print("\nCLEAR STORE")
store.clear()
print("Count:", store.count())