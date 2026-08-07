from backend.app.models.emotion import Emotion


class EmotionStore:
    """
    Stores detected emotions.
    """

    def __init__(self):

        self._emotions: list[Emotion] = []

    def add(
        self,
        emotion: Emotion,
    ):

        self._emotions.append(emotion)

    def get_all(self) -> list[Emotion]:

        return self._emotions

    def get_by_memory(
        self,
        memory_id: str,
    ) -> list[Emotion]:

        return [

            emotion

            for emotion in self._emotions

            if emotion.memory_id == memory_id

        ]

    def get_latest(
        self,
    ) -> Emotion | None:

        if not self._emotions:
            return None

        return self._emotions[-1]

    def count(
        self,
    ) -> int:

        return len(self._emotions)

    def clear(
        self,
    ):

        self._emotions.clear()