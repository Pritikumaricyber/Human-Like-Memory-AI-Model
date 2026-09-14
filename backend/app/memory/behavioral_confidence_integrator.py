from backend.app.memory.behavioral_confidence import (
    calculate_behavioral_confidence,
)

from backend.app.memory.behavioral_evidence_aggregator import (
    aggregate_behavioral_evidence,
)


def calculate_integrated_confidence(
    evidence: list[dict],
    base_confidence: float = 0.50,
) -> dict:
    """
    Calculate behavioral confidence using both
    evidence repetition and evidence consistency.
    """

    aggregation = aggregate_behavioral_evidence(
        evidence
    )

    total_count = aggregation["total_count"]

    if total_count == 0:
        return {
            **aggregation,
            "base_confidence": base_confidence,
            "confidence": 0.0,
        }

    repetition_confidence = (
        calculate_behavioral_confidence(
            signal_direction=(
                aggregation["net_direction"]
                if aggregation["net_direction"] != "conflicted"
                else "positive"
            ),
            evidence_count=total_count,
            base_confidence=base_confidence,
        )
    )

    consistency = aggregation["consistency"]

    confidence = (
        repetition_confidence * 0.60
        + consistency * 0.40
    )

    return {
        **aggregation,
        "base_confidence": base_confidence,
        "repetition_confidence": repetition_confidence,
        "confidence": round(
            min(1.0, max(0.0, confidence)),
            4,
        ),
    }