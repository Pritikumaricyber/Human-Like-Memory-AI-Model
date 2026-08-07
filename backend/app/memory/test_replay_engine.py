from backend.app.models.memory import Memory
from backend.app.models.emotion import Emotion

from backend.app.storage.emotion_store import EmotionStore

from backend.app.memory.replay_engine import replay_memories
from backend.app.memory.emotion_engine import apply_emotion


memories = [

    Memory(
        user_id="1",
        content="I use Python.",
        strength=0.95,
        importance=0.90
    ),

    Memory(
        user_id="1",
        content="I like tea.",
        strength=0.30,
        importance=0.20
    ),

    Memory(
        user_id="1",
        content="I study AI.",
        strength=0.85,
        importance=0.80
    ),

    Memory(
        user_id="1",
        content="I enjoy FastAPI.",
        strength=0.70,
        importance=0.60
    ),

    Memory(
        user_id="1",
        content="I visited Ranchi.",
        strength=0.40,
        importance=0.30
    )

]


emotion_store = EmotionStore()


joy = Emotion(
    user_id="1",
    memory_id=memories[2].id,
    emotion="joy",
    intensity=0.95,
    valence=0.90,
    arousal=0.85,
)

fear = Emotion(
    user_id="1",
    memory_id=memories[4].id,
    emotion="fear",
    intensity=0.90,
    valence=-0.90,
    arousal=0.95,
)


emotion_store.add(joy)
emotion_store.add(fear)


memories[2] = apply_emotion(
    memories[2],
    joy,
)

memories[4] = apply_emotion(
    memories[4],
    fear,
)


dreams = replay_memories(
    memories,
    emotion_store=emotion_store,
)


print("\n==============================")
print("MEMORY REPLAY")
print("==============================\n")


for memory in dreams:

    print(memory.content)

    print(
        "Strength :",
        round(memory.strength, 2)
    )

    print(
        "Importance :",
        round(memory.importance, 2)
    )

    emotion = emotion_store.get_by_memory(
        memory.id
    )

    if emotion:

        print(
            "Emotion :",
            emotion[-1].emotion
        )

        print(
            "Intensity :",
            emotion[-1].intensity
        )

    print()