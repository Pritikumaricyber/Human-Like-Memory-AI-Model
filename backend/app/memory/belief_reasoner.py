from backend.app.models.belief import Belief
from backend.app.models.memory import Memory

from backend.app.memory.belief_conflict_detector import (
    detect_belief_conflict,
)

from backend.app.memory.confidence_calibrator import (
    calibrate_confidence,
)

from backend.app.memory.belief_matcher import (
    calculate_belief_similarity,
)


# ============================================================
# THRESHOLDS
# ============================================================

REFINEMENT_THRESHOLD = 0.55
SUPPORT_THRESHOLD = 0.65
UNRELATED_THRESHOLD = 0.30


# ============================================================
# CONTRADICTION PHRASES
# ============================================================

CONTRADICTION_PHRASES = [
    "don't",
    "do not",
    "doesn't",
    "does not",
    "didn't",
    "did not",
    "no longer",
    "stopped",
    "hate",
    "hates",
    "dislike",
    "dislikes",
    "not anymore",
    "never",
]


# ============================================================
# CONTRADICTION SIGNAL
# ============================================================

def has_contradiction_signal(
    text: str,
) -> bool:
    """
    Detect simple linguistic signals that may indicate
    contradiction or reversal of a belief.
    """

    text_lower = text.lower()

    return any(
        phrase in text_lower
        for phrase in CONTRADICTION_PHRASES
    )


# ============================================================
# CLASSIFY RELATIONSHIP
# ============================================================

def classify_belief_relationship(
    belief: Belief,
    memory: Memory,
    similarity: float,
) -> str:
    """
    Classify the relationship between a memory
    and an existing belief.

    Possible relationships:

        support
        contradict
        refinement
        unrelated
    """

    # --------------------------------------------------------
    # 1. CONTRADICTION
    # --------------------------------------------------------

    if has_contradiction_signal(
        memory.content
    ):

        if similarity >= REFINEMENT_THRESHOLD:

            return "contradict"

    # --------------------------------------------------------
    # 2. VERY LOW SIMILARITY
    # --------------------------------------------------------

    if similarity < UNRELATED_THRESHOLD:

        return "unrelated"

    # --------------------------------------------------------
    # 3. EXISTING CONFLICT DETECTOR
    # --------------------------------------------------------

    conflict = detect_belief_conflict(
        belief,
        memory,
    )

    if conflict:

        return "contradict"

    # --------------------------------------------------------
    # 4. HIGH SIMILARITY
    # --------------------------------------------------------
    #
    # Even if the memory is identical to the belief,
    # it represents additional supporting evidence.
    #
    # Duplicate belief creation is handled separately
    # by the KnowledgeManager.
    # --------------------------------------------------------

    if similarity >= SUPPORT_THRESHOLD:

        return "support"

    # --------------------------------------------------------
    # 5. MODERATE SIMILARITY
    # --------------------------------------------------------

    if similarity >= REFINEMENT_THRESHOLD:

        return "refinement"

    # --------------------------------------------------------
    # 6. FALLBACK
    # --------------------------------------------------------

    return "unrelated"


# ============================================================
# REASON ABOUT BELIEF
# ============================================================

def reason_about_belief(
    belief: Belief,
    memory: Memory,
) -> dict:
    """
    Decide how a belief should evolve after
    receiving new evidence.

    The reasoning process considers:

    - semantic similarity
    - contradiction signals
    - existing conflict detection
    - evidence relationship
    - confidence calibration
    """

    # --------------------------------------------------------
    # STEP 1 : SEMANTIC SIMILARITY
    # --------------------------------------------------------

    similarity = calculate_belief_similarity(
        memory.content,
        belief.belief,
    )

    # --------------------------------------------------------
    # STEP 2 : CLASSIFY RELATIONSHIP
    # --------------------------------------------------------

    relationship = classify_belief_relationship(
        belief,
        memory,
        similarity,
    )

    # --------------------------------------------------------
    # STEP 3 : UNRELATED
    # --------------------------------------------------------

    if relationship == "unrelated":

        return {
            "action": "ignore",
            "conflict": False,
            "relationship": "unrelated",
            "new_confidence": belief.confidence,
            "state": belief.state,
            "similarity": similarity,
        }

    # --------------------------------------------------------
    # STEP 4 : CONTRADICTION
    # --------------------------------------------------------

    if relationship == "contradict":

        new_confidence = calibrate_confidence(
            belief.confidence,
            True,
        )

        return {
            "action": "weaken",
            "conflict": True,
            "relationship": "contradict",
            "new_confidence": new_confidence,
            "state": "contested",
            "similarity": similarity,
        }

    # --------------------------------------------------------
    # STEP 5 : SUPPORT
    # --------------------------------------------------------

    if relationship == "support":

        new_confidence = calibrate_confidence(
            belief.confidence,
            False,
        )

        return {
            "action": "strengthen",
            "conflict": False,
            "relationship": "support",
            "new_confidence": new_confidence,
            "state": "supported",
            "similarity": similarity,
        }

    # --------------------------------------------------------
    # STEP 6 : REFINEMENT
    # --------------------------------------------------------

    if relationship == "refinement":

        new_confidence = min(
            1.0,
            belief.confidence + 0.05,
        )

        return {
            "action": "refine",
            "conflict": False,
            "relationship": "refinement",
            "new_confidence": new_confidence,
            "state": belief.state,
            "similarity": similarity,
        }

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return {
        "action": "ignore",
        "conflict": False,
        "relationship": "unrelated",
        "new_confidence": belief.confidence,
        "state": belief.state,
        "similarity": similarity,
    }