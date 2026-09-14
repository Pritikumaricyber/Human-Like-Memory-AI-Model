import re


PREFERENCE_CHANGE_PATTERNS = [
   r"\bnow\s+prefers?\s+([A-Za-z0-9_.+#-]+)(?:\s+for\s+[A-Za-z0-9_.+#-]+)?\s+(?:instead of|over)\s+([A-Za-z0-9_.+#-]+)",
   r"\bprefers?\s+([A-Za-z0-9_.+#-]+)(?:\s+for\s+[A-Za-z0-9_.+#-]+)?\s+(?:instead of|over)\s+([A-Za-z0-9_.+#-]+)",
]


def detect_preference_change(text: str) -> dict | None:
    """
    Detect explicit preference changes in both
    user messages and normalized memory statements.

    Examples:

        I now prefer Java for programming instead of Python.
        I prefer Java over Python.
        The user prefers Java for programming over Python.

    Returns the new preferred concept and the
    superseded concept.
    """

    for pattern in PREFERENCE_CHANGE_PATTERNS:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return {
                "new_preference": match.group(1).lower().rstrip(".,!?"),
                "superseded_preference": match.group(2).lower().rstrip(".,!?"),
            }

    return None