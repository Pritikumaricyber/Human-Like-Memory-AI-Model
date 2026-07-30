from backend.app.models.memory import Memory
from backend.app.memory.decay_engine import apply_decay
from backend.app.memory.forgetting_engine import decide_forgetting


def run_memory_scheduler(
    memories: list[Memory]
) -> list[Memory]:
    """
    Run periodic maintenance on all memories.
    """

    updated_memories = []

    for memory in memories:

        # Apply memory decay
        apply_decay(memory)

        # Decide what to do with the memory
        decision = decide_forgetting(memory)

        if decision == "keep":
            updated_memories.append(memory)

        elif decision == "archive":
            memory.status = "archived"
            updated_memories.append(memory)

        elif decision == "forget":
            # Skip adding it → effectively forgotten
            continue

    return updated_memories