class WorkingMemory:
    """
    Temporary memory used for current reasoning.
    """

    def __init__(self, capacity=7):
        self.capacity = capacity
        self.memories = []

    def add(self, memory):
        """
        Add a memory into working memory.
        """

        if len(self.memories) >= self.capacity:
            self.memories.pop(0)

        self.memories.append(memory)

    def retrieve_all(self):
        return self.memories

    def clear(self):
        self.memories.clear()

    def size(self):
        return len(self.memories)