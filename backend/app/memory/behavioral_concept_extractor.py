import re

CONTEXT_WORDS = {
    "i","am","my","me","user","the","a","an","is","are","for","with","to",
    "anymore","now","working","work","using","use","learn","studying","study",
    "practice","practicing","language","strongly","programming",
}


def extract_concept(text, matched_phrase):
    text_without_signal = re.sub(
        rf"\b{re.escape(matched_phrase)}\b",
        " ",
        text,
        count=1,
        flags=re.IGNORECASE,
    ) if matched_phrase.lower() != "using" else text

    # For natural usage statements such as
    # "I usually build AI projects using Python",
    # the concept is the technology after "using".
    using_match = re.search(
        r"\busing\s+([A-Za-z0-9_.+#-]+)",
        text_without_signal,
        flags=re.IGNORECASE,
    )

    if using_match:
        return using_match.group(1).strip().rstrip(".")
    text_without_signal = re.sub(
        r"[^\w\s]",
        " ",
        text_without_signal,
    )

    words = text_without_signal.split()

    concept_words = [
        word
        for word in words
        if word.lower() not in CONTEXT_WORDS
    ]

    if not concept_words:
        return None

    return " ".join(concept_words).strip()