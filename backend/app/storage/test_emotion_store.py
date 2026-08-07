from backend.app.models.emotion import Emotion
from backend.app.storage.emotion_store import EmotionStore


store = EmotionStore()

store.add(

    Emotion(
        user_id="user_001",
        memory_id="m1",
        emotion="joy",
        intensity=0.9,
        valence=0.9,
        arousal=0.8,
    )

)

store.add(

    Emotion(
        user_id="user_001",
        memory_id="m2",
        emotion="fear",
        intensity=0.8,
        valence=-0.9,
        arousal=0.95,
    )

)

print("\n==============================")
print("EMOTION STORE")
print("==============================\n")

print("Total emotions:", store.count())

print("\nStored emotions:\n")

for emotion in store.get_all():

    print(
        emotion.memory_id,
        "->",
        emotion.emotion
    )

print("\nLatest emotion:")

latest = store.get_latest()

print(latest.emotion)