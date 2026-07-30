from backend.app.memory.decay_engine import (
    calculate_decay,
    reinforce_memory
)


strength = 0.80
decay_rate = 0.02


print("\n==============================")
print("MEMORY DECAY")
print("==============================")


for days in [0, 10, 30, 60, 100]:

    result = calculate_decay(
        strength=strength,
        decay_rate=decay_rate,
        days_since_recall=days
    )

    print(
        f"After {days:3} days → "
        f"Strength: {result:.4f}"
    )


print("\n==============================")
print("MEMORY REINFORCEMENT")
print("==============================")


current_strength = 0.50

for recall in range(1, 5):

    current_strength = reinforce_memory(
        current_strength
    )

    print(
        f"Recall {recall} → "
        f"Strength: {current_strength:.4f}"
    )
    