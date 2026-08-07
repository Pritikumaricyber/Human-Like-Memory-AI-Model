from backend.app.models.memory import Memory
from backend.app.memory.forgetting_engine import decide_forgetting
from backend.app.memory.memory_decay import apply_memory_decay


class ForgettingManager:
    """
    Applies forgetting decisions to memories.

    Possible outcomes:
    - active
    - dormant
    - forgotten
    """

    def process_memory(
        self,
        memory: Memory,
    ) -> Memory:

        decision = decide_forgetting(memory)

        if decision == "active":
            memory.status = "active"

        elif decision == "dormant":
            memory.status = "dormant"
            apply_memory_decay(memory)

        elif decision == "forgotten":
            memory.status = "forgotten"
            memory.strength = 0.0

        return memory