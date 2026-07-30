from backend.app.models.belief import Belief
from backend.app.models.evidence import Evidence
from backend.app.memory.belief_updater import update_belief


def run_test(label, relationship):

    belief = Belief(
        user_id="user_001",
        subject="user_001",
        belief="User prefers Python",
        confidence=0.70,
        currentness=1.0,
        state="supported"
    )

    evidence = Evidence(
        user_id="user_001",
        content="Test evidence",
        evidence_type="statement",
        relationship=relationship,
        reliability=0.90,
        specificity=0.90,
        independence=0.80
    )

    print("\n==============================")
    print(label)
    print("==============================")

    print("BEFORE")
    print("Confidence:", belief.confidence)
    print("Currentness:", belief.currentness)
    print("State:", belief.state)

    updated = update_belief(
        belief,
        evidence
    )

    print("\nAFTER")
    print("Confidence:", updated.confidence)
    print("Currentness:", updated.currentness)
    print("State:", updated.state)


run_test("SUPPORT", "support")
run_test("CONTRADICTION", "contradict")
run_test("REFINEMENT", "refinement")
run_test("DUPLICATE", "duplicate")
run_test("UNRELATED", "unrelated")