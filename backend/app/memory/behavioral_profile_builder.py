from collections import defaultdict

from backend.app.memory.behavioral_confidence_integrator import (
    calculate_integrated_confidence,
)


def build_behavioral_profile(evidence: list[dict]) -> dict:
    """
    Build a behavioral profile from observations belonging
    to one concept.

    Superseded observations remain part of historical memory,
    but they do not contribute to the current behavioral profile.
    """

    if not evidence:
        return {
            "concept": None,
            "behavior": None,
            "direction": None,
            "evidence_count": 0,
            "consistency": 0.0,
            "confidence": 0.0,
            "behavior_profiles": [],
        }

    concept = evidence[0].get("concept")

    active_evidence = [
        item
        for item in evidence
        if not item.get("superseded", False)
    ]

    if not active_evidence:
        return {
            "concept": concept,
            "behavior": None,
            "direction": None,
            "evidence_count": 0,
            "consistency": 0.0,
            "confidence": 0.0,
            "behavior_profiles": [],
        }

    grouped_evidence = defaultdict(list)

    for item in active_evidence:
        grouped_evidence[item.get("behavior")].append(item)

    behavior_profiles = []

    for behavior, behavior_evidence in grouped_evidence.items():

        confidence_result = calculate_integrated_confidence(
            behavior_evidence
        )

        behavior_profiles.append(
            {
                "behavior": behavior,
                "direction": confidence_result["net_direction"],
                "evidence_count": confidence_result["total_count"],
                "consistency": confidence_result["consistency"],
                "confidence": confidence_result["confidence"],
            }
        )

    primary_profile = behavior_profiles[0]

    return {
        "concept": concept,
        "behavior": primary_profile["behavior"],
        "direction": primary_profile["direction"],
        "evidence_count": primary_profile["evidence_count"],
        "consistency": primary_profile["consistency"],
        "confidence": primary_profile["confidence"],
        "behavior_profiles": behavior_profiles,
    }