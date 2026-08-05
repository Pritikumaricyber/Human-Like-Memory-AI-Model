from backend.app.memory.semantic_generalizer import (
    semantic_generalize,
)

clusters = {

    "python": [
        "python",
        "fastapi",
        "api"
    ],

    "ai": [
        "ai",
        "machine",
        "learning"
    ],

    "ranchi": [
        "ranchi"
    ]
}

generalized = semantic_generalize(clusters)

print("\n==============================")
print("SEMANTIC GENERALIZER")
print("==============================\n")

for topic, concepts in generalized.items():

    print(topic)

    print(concepts)

    print()