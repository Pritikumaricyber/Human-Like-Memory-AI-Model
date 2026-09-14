from backend.app.models.memory import Memory

from backend.app.memory.forgetting_engine import (
    decide_forgetting,
    calculate_memory_retention,
)

from backend.app.memory.memory_decay import (
    apply_memory_decay,
)


class ForgettingManager:
    """
    Manages the lifecycle of memories.

    Memory states:

        active
        dormant
        forgotten

    The manager combines retention scoring
    with memory decay.
    """

    def process_memory(
        self,
        memory: Memory,
    ) -> Memory:

        # -----------------------------------------------------
        # CURRENT USER PREFERENCE
        # -----------------------------------------------------

        # Explicit active preferences represent the user's
        # current state and should not fade through forgetting.
        if (
            memory.memory_type == "preference"
            and memory.status == "active"
        ):
            return memory

        # -----------------------------------------------------
        # Calculate retention
        # -----------------------------------------------------

        retention = calculate_memory_retention(
            memory
        )

        # -----------------------------------------------------
        # Decide lifecycle state
        # -----------------------------------------------------

        decision = decide_forgetting(
            memory
        )

        # -----------------------------------------------------
        # ACTIVE
        # -----------------------------------------------------

        if decision == "active":

            memory.status = "active"

        # -----------------------------------------------------
        # DORMANT
        # -----------------------------------------------------

        elif decision == "dormant":

            memory.status = "dormant"

            apply_memory_decay(
                memory
            )

        # -----------------------------------------------------
        # FORGOTTEN
        # -----------------------------------------------------

        elif decision == "forgotten":

            memory.status = "forgotten"

            memory.strength = 0.0

        # -----------------------------------------------------
        # DEBUG INFORMATION
        # -----------------------------------------------------

        print(
            f"Retention: {retention:.3f} | "
            f"Decision: {decision}"
        )

        return memory
