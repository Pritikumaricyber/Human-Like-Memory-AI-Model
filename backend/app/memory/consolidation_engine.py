from backend.app.memory.evidence_analyzer import (
    classify_relationship,
    calculate_semantic_similarity,
)


def consolidate_memory(new_memory, old_memories):
    """
    Compare a new memory with existing memories.
    """

    results = []

    

    for memory in old_memories:

        

        similarity = calculate_semantic_similarity(
            memory.content,
            new_memory.content
        )

        relationship = classify_relationship(
            memory.content,
            new_memory.content,
            similarity
        )

        independence = max(
            0.0,
            min(1.0, 1.0 - similarity)
        )

        results.append({
            "memory": memory,
            "relationship": relationship,
            "independence": independence
        })

    return results