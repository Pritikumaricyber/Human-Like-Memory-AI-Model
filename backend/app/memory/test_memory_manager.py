from backend.app.models.memory import Memory
from backend.app.memory.memory_manager import MemoryManager


stored_memories = [

    Memory(
        user_id="user_001",
        content="I use Python for AI.",
        memory_type="fact",
        importance=0.8,
        confidence=0.9,
        strength=0.8,
        emotional_score=0.2,
    ),

    Memory(
        user_id="user_001",
        content="I visited Ranchi yesterday.",
        memory_type="event",
        importance=0.5,
        confidence=0.9,
        strength=0.5,
        emotional_score=0.1,
    ),
]

new_memory = Memory(
    user_id="user_001",
    content="Python is my favorite language.",
    memory_type="fact",
    importance=0.8,
    confidence=0.9,
    strength=0.7,
    emotional_score=0.2,
)

manager = MemoryManager()
#Sprint(type(manager.belief_store).__name__)

for memory in stored_memories:
    manager.memory_store.add(memory)

result = manager.process_memory(new_memory)

print("\n==============================")
print("MEMORY MANAGER")
print("==============================")

print("\nRETRIEVED MEMORIES\n")

for item in result["retrieved"]:
    print(item["memory"].content)
    print("Score:", round(item["retrieval_score"], 4))
    print()

print("\nCONSOLIDATION\n")

for item in result["consolidation"]:
    print(item["memory"].content)
    print("Relationship :", item["relationship"])
    print("Independence :", round(item["independence"], 4))
    print()
    
print("\nDECISION\n")

print("Action :", result["decision"]["action"])

if result["decision"]["target"] is not None:
    print("Target :", result["decision"]["target"].content)

if "relationship" in result["decision"]:
    print("Relationship :", result["decision"]["relationship"])