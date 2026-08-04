from backend.app.models.memory import Memory

from backend.app.memory.decay_engine import apply_decay
from backend.app.memory.forgetting_engine import decide_forgetting


def run_forgetting_scheduler(
    memories: list[Memory]
) -> list[Memory]:
    """
    Simulates one complete forgetting cycle.

    For every memory:
    1. Apply human-like decay.
    2. Decide its new lifecycle state.
    """

    updated_memories = []

    for memory in memories:

        # Gradually weaken the memory
        memory = apply_decay(memory)

        # Decide its lifecycle state
        memory.status = decide_forgetting(memory)

        updated_memories.append(memory)

    return updated_memories