from backend.app.memory.memory_manager import MemoryManager


mm = MemoryManager()

memories = mm.memory_store.get_all()

print("\n==============================")
print("FORGOTTEN MEMORY RETRIEVAL TEST")
print("==============================")

print("\nCURRENT MEMORIES:")
for memory in memories:
    print(
        f"- {memory.content} | "
        f"status={memory.status}"
    )

# ---------------------------------------------------------
# Find the Ranchi memory
# ---------------------------------------------------------

target = next(
    (
        memory
        for memory in memories
        if "Ranchi" in memory.content
    ),
    None,
)

if target is None:
    print("\nERROR: Ranchi memory not found.")
    raise SystemExit

# ---------------------------------------------------------
# Temporarily mark it forgotten
# ---------------------------------------------------------

original_status = target.status
target.status = "forgotten"

mm.memory_store.update(target)

print(
    f"\nMarked as forgotten: "
    f"{target.content}"
)

# ---------------------------------------------------------
# Retrieve memories
# ---------------------------------------------------------

results = mm.retrieve_relevant_memories(
    user_id="user_001",
    query="Where did I go yesterday?",
    top_k=5,
)

print("\nRETRIEVED MEMORIES:")

for index, memory in enumerate(results, start=1):
    print(
        f"{index}. {memory.content} | "
        f"status={memory.status}"
    )

# ---------------------------------------------------------
# Verify forgotten memory is excluded
# ---------------------------------------------------------

forgotten_found = any(
    memory.id == target.id
    for memory in results
)

if forgotten_found:
    print("\n❌ TEST FAILED")
    print("Forgotten memory was retrieved.")

else:
    print("\n✅ TEST PASSED")
    print("Forgotten memory was correctly excluded.")

# ---------------------------------------------------------
# Restore original status
# ---------------------------------------------------------

target.status = original_status
mm.memory_store.update(target)

print(
    f"\nRestored: "
    f"{target.content} | "
    f"status={target.status}"
)