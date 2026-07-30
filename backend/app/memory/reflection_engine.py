from collections import Counter


def reflect(episodes):
    """
    Convert repeated episodes into semantic knowledge.
    """

    keyword_counter = Counter()

    for episode in episodes:

        text = episode["memory"].content.lower()

        words = text.split()

        keyword_counter.update(words)

    learned_beliefs = []

    if keyword_counter["python"] >= 2:
        learned_beliefs.append(
            "User prefers Python."
        )

    if keyword_counter["ai"] >= 2:
        learned_beliefs.append(
            "User frequently works on AI."
        )

    if keyword_counter["javascript"] >= 2:
        learned_beliefs.append(
            "User prefers JavaScript."
        )

    return learned_beliefs