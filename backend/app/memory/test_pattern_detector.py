from backend.app.models.memory import Memory

from backend.app.memory.pattern_detector import (
    detect_patterns,
)

memories = [

    Memory(
        user_id="1",
        content="I use Python for AI."
    ),

    Memory(
        user_id="1",
        content="Python is my favorite language."
    ),

    Memory(
        user_id="1",
        content="AI is changing software."
    ),

    Memory(
        user_id="1",
        content="FastAPI works well with Python."
    )

]

patterns = detect_patterns(memories)

print("\n==============================")
print("PATTERN DETECTOR")
print("==============================\n")

for word, count in sorted(
    patterns.items(),
    key=lambda x: x[1],
    reverse=True
):

    if count >= 2:

        print(f"{word} -> {count}")
        