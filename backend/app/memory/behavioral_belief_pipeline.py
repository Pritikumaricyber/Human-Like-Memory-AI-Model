from backend.app.memory.behavioral_inference_builder import (
    build_behavioral_inference
)
from backend.app.memory.behavioral_confidence_integrator import (
    calculate_integrated_confidence
)
from backend.app.memory.behavioral_evidence_builder import (
    build_behavioral_evidence
)
from backend.app.memory.behavioral_belief_matcher import (
    match_behavioral_belief
)
from backend.app.memory.behavioral_belief_reasoner import (
    reason_about_behavioral_inference
)
from backend.app.memory.behavioral_belief_updater import (
    update_behavioral_belief
)
from backend.app.memory.belief_history_manager import (
    record_belief_change
)


def process_behavioral_statement(
    user_id: str,
    text: str,
    beliefs: list
):
    """
    Process a user statement through the behavioral
    inference and belief pipeline.

    Returns:
        pipeline result dictionary
    """

    # Step 1: Build behavioral inference
    inference = build_behavioral_inference(text)

    if inference is not None:
        inference["user_id"] = user_id

    if inference is None:
        return {
            "inference": None,
            "belief": None,
            "evidence": None,
            "reasoning": None,
            "history": None,
        }

    # Step 2: Find matching belief
    belief, similarity = match_behavioral_belief(
        inference,
        beliefs
    )

    # No existing belief to update
    if belief is None:
        return {
            "inference": inference,
            "belief": None,
            "evidence": None,
            "reasoning": None,
            "history": None,
            "similarity": similarity,
        }

    # Step 3: Collect behavioral evidence
    evidence = build_behavioral_evidence(
        inference,
        confidence=0.50
    )

    # Step 4: Reason about the behavioral inference
    reasoning = reason_about_behavioral_inference(
        belief,
        inference
    )

    # Step 5: Update belief using reasoning result
    old_belief = belief.model_copy(deep=True)

    updated_belief = update_behavioral_belief(
        belief,
        evidence,
        reasoning
    )

    # Step 6: Record belief evolution
    history = record_belief_change(
        old_belief,
        updated_belief,
        evidence
    )

    return {
        "inference": inference,
        "belief": updated_belief,
        "evidence": evidence,
        "reasoning": reasoning,
        "history": history,
        "similarity": similarity,
    }