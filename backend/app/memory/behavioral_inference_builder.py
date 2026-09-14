from email.mime import text
import signal

from backend.app.memory.behavioral_signal_detector import (
    detect_behavioral_signal,
)

from backend.app.memory.behavioral_concept_extractor import (
    extract_concept,
)
from backend.app.memory.behavioral_concept_normalizer import (
    normalize_behavioral_concept,
)
from backend.app.memory.behavioral_change_detector import (
    detect_preference_change,
)



def build_behavioral_inference(
    text: str,
) -> dict | None:
    """
    Build a structured behavioral inference
    from a memory text.
    """

    signal = detect_behavioral_signal(text)

    if signal is None:
        return None

    concept = extract_concept(
        text,
        signal["matched_phrase"],
    )
    concept = normalize_behavioral_concept(
        concept
    )

    if concept is None:
        return None
    
    preference_change = None
    if signal["signal_type"] == "preference":
        preference_change = detect_preference_change(text)
    if preference_change is not None:
        concept = preference_change["new_preference"]    

    behavior = signal["signal_type"]
    direction = signal["direction"]

    if behavior == "preference":

        if direction == "positive":
            inference = (
                f"User prefers {concept}."
            )
        else:
            inference = (
                f"User dislikes {concept}."
            )

    elif behavior == "usage":

        if direction == "positive":
            inference = (
                f"User frequently uses {concept}."
            )
        else:
            inference = (
                f"User no longer uses {concept}."
            )

    elif behavior == "learning":

        if direction == "positive":
            inference = (
                f"User is learning {concept}."
            )
        else:
            inference = (
                f"User is no longer learning {concept}."
            )

    else:
        inference = (
            f"User shows a {direction} "
            f"{behavior} toward {concept}."
        )
   
    return {
        "concept": concept,
        "behavior": behavior,
        "direction": direction,
        "inference": inference,
        "source_text": text,
        "matched_phrase": signal["matched_phrase"],
        "preference_change": preference_change,
    }