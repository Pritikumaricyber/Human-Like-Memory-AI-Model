from backend.app.models.memory import Memory

from backend.app.memory.episode_collector import collect_episodes
from backend.app.memory.pattern_miner import mine_patterns


memories = [

    Memory(
        user_id="user_001",
        content="Python is great",
        memory_type="fact"
    ),

    Memory(
        user_id="user_001",
        content="Python is useful",
        memory_type="fact"
    ),

    Memory(
        user_id="user_001",
        content="Ranchi is beautiful",
        memory_type="fact"
    ),

    Memory(
        user_id="user_001",
        content="Ranchi has waterfalls",
        memory_type="fact"
    ),
]

episodes = collect_episodes(memories)

patterns = mine_patterns(episodes)

print("\n==============================")
print("PATTERN MINER")
print("==============================\n")

for topic, counter in patterns.items():

    print(topic)

    print(dict(counter))

    print()
    