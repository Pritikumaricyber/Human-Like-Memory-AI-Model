from backend.app.memory.emotion_detector import detect_emotion


examples = [

    "I got my internship today!",

    "I failed my exam.",

    "I almost had an accident.",

    "I am furious with my manager.",

    "Python is useful.",

]

print("\n==============================")
print("EMOTION DETECTOR")
print("==============================\n")

for sentence in examples:

    emotion = detect_emotion(
        user_id="user_001",
        memory_id="memory_001",
        text=sentence,
    )

    print(sentence)
    print("Emotion  :", emotion.emotion)
    print("Intensity:", emotion.intensity)
    print("Valence  :", emotion.valence)
    print("Arousal  :", emotion.arousal)
    print()