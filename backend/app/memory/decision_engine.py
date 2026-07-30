def make_memory_decision(consolidation_results):
    """
    Decide what should happen after memory consolidation.
    """

    if not consolidation_results:
        return {
            "action": "store_new",
            "target": None,
            "relationship": None,
            "independence": None,
        }

    # Best match = lowest independence
    best_match = min(
        consolidation_results,
        key=lambda x: x["independence"]
    )

    relationship = best_match["relationship"]

    if relationship == "duplicate":
        action = "ignore"

    elif relationship == "support":
        action = "strengthen_belief"

    elif relationship == "refinement":
        action = "update_memory"

    elif relationship == "contradiction":
        action = "revise_belief"

    else:
        action = "store_new"

    return {
        "action": action,
        "target": best_match["memory"],
        "relationship": relationship,
        "independence": best_match["independence"],
    }