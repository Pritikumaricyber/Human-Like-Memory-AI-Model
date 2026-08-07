from backend.app.models.emotion import Emotion


emotion = Emotion(
    user_id="user_001",
    memory_id="memory_001",
    emotion="joy",
    intensity=0.92,
    valence=0.90,
    arousal=0.75,
)

print("\n==============================")
print("EMOTION MODEL")
print("==============================\n")

print("Emotion   :", emotion.emotion)
print("Intensity :", emotion.intensity)
print("Valence   :", emotion.valence)
print("Arousal   :", emotion.arousal)