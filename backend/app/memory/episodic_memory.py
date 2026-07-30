from datetime import datetime


class EpisodicMemory:
    """
    Stores personal experiences (episodes).
    """

    def __init__(self):
        self.episodes = []

    def add_episode(self, memory):
        """
        Store a new episode.
        """

        episode = {
            "memory": memory,
            "timestamp": datetime.now()
        }

        self.episodes.append(episode)

    def retrieve_all(self):
        """
        Return all stored episodes.
        """

        return self.episodes

    def size(self):
        return len(self.episodes)

    def clear(self):
        self.episodes.clear()