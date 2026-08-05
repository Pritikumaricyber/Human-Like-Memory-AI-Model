from backend.app.memory.replay_engine import replay_memories
from backend.app.memory.episode_collector import collect_episodes
from backend.app.memory.pattern_miner import mine_patterns
from backend.app.memory.concept_clusterer import cluster_concepts
from backend.app.memory.semantic_generalizer import (
    semantic_generalize,
)
from backend.app.memory.generalization_engine import (
    generalize,
)


def run_semantic_learning(
    memories,
    user_id: str,
):
    """
    Complete semantic learning pipeline.

    Converts episodic memories into
    long-term semantic beliefs.
    """

    replayed = replay_memories(memories)

    episodes = collect_episodes(replayed)

    patterns = mine_patterns(episodes)

    clusters = cluster_concepts(patterns)

    semantic = semantic_generalize(clusters)

    beliefs = generalize(
        semantic,
        user_id=user_id,
    )

    return beliefs