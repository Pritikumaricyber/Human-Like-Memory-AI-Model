from backend.app.models.memory import Memory

from backend.app.memory.episode_collector import collect_episodes
from backend.app.memory.pattern_miner import mine_patterns
from backend.app.memory.concept_clusterer import cluster_concepts
from backend.app.memory.generalization_engine import generalize


memories = [

    Memory(
        user_id="user_001",
        content="Python is great",
        memory_type="fact",
    ),

    Memory(
        user_id="user_001",
        content="Python is useful",
        memory_type="fact",
    ),

    Memory(
        user_id="user_001",
        content="Ranchi is beautiful",
        memory_type="fact",
    ),

    Memory(
        user_id="user_001",
        content="Ranchi has waterfalls",
        memory_type="fact",
    ),
]

episodes = collect_episodes(memories)

patterns = mine_patterns(episodes)

clusters = cluster_concepts(patterns)

beliefs = generalize(
    clusters,
    user_id="user_001",
)

print("\n==============================")
print("GENERALIZATION ENGINE")
print("==============================\n")

for belief in beliefs:

    print("Subject   :", belief.subject)
    print("Belief    :", belief.belief)
    print("Confidence:", belief.confidence)
    print()