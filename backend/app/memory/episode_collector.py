from collections import defaultdict

from backend.app.models.memory import Memory


def collect_episodes(
    memories: list[Memory],
) -> dict[str, list[Memory]]:
    """
    Group episodic memories by their first keyword.

    Later this will be replaced by semantic clustering,
    but this provides a clean interface for the pipeline.
    """

    episodes = defaultdict(list)

    for memory in memories:

        key = memory.content.split()[0].lower()

        episodes[key].append(memory)

    return dict(episodes)
