from backend.app.models.belief_history import BeliefHistory


def analyze_belief_evolution(
    history: list[BeliefHistory],
) -> str:
    """
    Analyze how a belief has evolved over time.

    Returns one of:

    - stable
    - strengthening
    - declining
    - unstable
    - superseded

    The analysis uses existing belief history records.
    """

    if not history:
        return "stable"

    # Sort chronologically so evolution is evaluated
    # from the oldest change to the newest change.
    ordered_history = sorted(
        history,
        key=lambda record: record.created_at,
    )

    # -----------------------------------------
    # SUPPORTED / SUPERSEDED STATES
    # -----------------------------------------

    latest_state = ordered_history[-1].new_state

    if latest_state == "superseded":
        return "superseded"

    # -----------------------------------------
    # CONFIDENCE CHANGES
    # -----------------------------------------

    changes = [
        record.new_confidence - record.previous_confidence
        for record in ordered_history
    ]

    positive_changes = sum(
        1 for change in changes
        if change > 0
    )

    negative_changes = sum(
        1 for change in changes
        if change < 0
    )

    # -----------------------------------------
    # STABLE
    # -----------------------------------------

    if all(
        abs(change) < 0.01
        for change in changes
    ):
        return "stable"

    # -----------------------------------------
    # UNSTABLE
    # -----------------------------------------

    if (
        positive_changes > 0
        and negative_changes > 0
    ):
        return "unstable"

    # -----------------------------------------
    # STRENGTHENING
    # -----------------------------------------

    if positive_changes > 0:
        return "strengthening"

    # -----------------------------------------
    # DECLINING
    # -----------------------------------------

    if negative_changes > 0:
        return "declining"

    return "stable"