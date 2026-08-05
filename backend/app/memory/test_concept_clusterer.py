from backend.app.models.memory import Memory

from backend.app.memory.episode_collector import collect_episodes
from backend.app.memory.pattern_miner import mine_patterns
from backend.app.memory.concept_clusterer import cluster_concepts


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

print("\n==============================")
print("CONCEPT CLUSTERER")
print("==============================\n")

for topic, concepts in clusters.items():

    print(topic)

    print(concepts)

    print()