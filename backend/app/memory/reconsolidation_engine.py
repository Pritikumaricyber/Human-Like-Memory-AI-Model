from datetime import datetime

from backend.app.models.memory import Memory


def reconsolidate_memory(
    memory: Memory,
    new_content: str
) -> Memory:
    """
    Update an existing memory after it has
    been recalled and new information is received.
    """

    # Update memory content
    memory.content = new_content

    # Strengthen the memory
    memory.strength = min(
        1.0,
        memory.strength + 0.10
    )

    # Increase confidence
    memory.confidence = min(
        1.0,
        memory.confidence + 0.05
    )

    # Increase recall count
    memory.recall_count += 1

    # Update recall time
    memory.last_recalled = datetime.now()

    return memory