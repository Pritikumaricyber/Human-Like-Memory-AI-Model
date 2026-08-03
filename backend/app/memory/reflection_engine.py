from collections import Counter

from backend.app.models.memory import Memory
from backend.app.models.belief import Belief
from backend.app.memory.belief_builder import build_belief


def reflect(memories: list[Memory]) -> list[Belief]:
    """
    Reflection Engine

    Converts repeated episodic memories
    into higher-level semantic beliefs.
    """

    keyword_counter = Counter()

    for memory in memories:

        words = memory.content.lower().split()

        keyword_counter.update(words)

    learned_beliefs = []

    # -----------------------------------------
    # Python
    # -----------------------------------------

    if keyword_counter["python"] >= 2:

        memory = Memory(
            user_id="reflection",
            content="User prefers Python.",
            memory_type="semantic",
            importance=0.8
        )

        learned_beliefs.append(
            build_belief(memory)
        )

    # -----------------------------------------
    # AI
    # -----------------------------------------

    if keyword_counter["ai"] >= 2:

        memory = Memory(
            user_id="reflection",
            content="User frequently works on AI.",
            memory_type="semantic",
            importance=0.8
        )

        learned_beliefs.append(
            build_belief(memory)
        )

    # -----------------------------------------
    # JavaScript
    # -----------------------------------------

    if keyword_counter["javascript"] >= 2:

        memory = Memory(
            user_id="reflection",
            content="User prefers JavaScript.",
            memory_type="semantic",
            importance=0.8
        )

        learned_beliefs.append(
            build_belief(memory)
        )

    return learned_beliefs