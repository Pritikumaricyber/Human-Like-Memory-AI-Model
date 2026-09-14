
from backend.app.memory.confidence_calibrator import (
    calibrate_confidence,
)


print("\n==============================")
print("CONFIDENCE CALIBRATOR TESTS")
print("==============================")


# =========================================================
# TEST 1 : SUPPORTING EVIDENCE
# =========================================================

print("\nTEST 1 : SUPPORTING EVIDENCE")

initial_confidence = 0.50

new_confidence = calibrate_confidence(
    current_confidence=initial_confidence,
    conflict=False,
)

print("Initial confidence :", initial_confidence)
print("New confidence     :", new_confidence)

assert new_confidence == 0.60

print("Supporting evidence increases confidence: PASS")


# =========================================================
# TEST 2 : CONTRADICTING EVIDENCE
# =========================================================

print("\nTEST 2 : CONTRADICTING EVIDENCE")

initial_confidence = 0.50

new_confidence = calibrate_confidence(
    current_confidence=initial_confidence,
    conflict=True,
)

print("Initial confidence :", initial_confidence)
print("New confidence     :", new_confidence)

assert new_confidence == 0.40

print("Contradicting evidence decreases confidence: PASS")


# =========================================================
# TEST 3 : UPPER BOUND
# =========================================================

print("\nTEST 3 : UPPER BOUND")

new_confidence = calibrate_confidence(
    current_confidence=0.95,
    conflict=False,
)

print("Initial confidence :", 0.95)
print("New confidence     :", new_confidence)

assert new_confidence == 1.0

print("Confidence capped at 1.0: PASS")


# =========================================================
# TEST 4 : LOWER BOUND
# =========================================================

print("\nTEST 4 : LOWER BOUND")

new_confidence = calibrate_confidence(
    current_confidence=0.05,
    conflict=True,
)

print("Initial confidence :", 0.05)
print("New confidence     :", new_confidence)

assert new_confidence == 0.0

print("Confidence capped at 0.0: PASS")


# =========================================================
# TEST 5 : CUSTOM LEARNING RATE
# =========================================================

print("\nTEST 5 : CUSTOM LEARNING RATE")

new_confidence = calibrate_confidence(
    current_confidence=0.50,
    conflict=False,
    learning_rate=0.20,
)

print("Initial confidence :", 0.50)
print("Learning rate      :", 0.20)
print("New confidence     :", new_confidence)

assert new_confidence == 0.70

print("Custom learning rate works: PASS")


# =========================================================
# TEST 6 : REPEATED SUPPORTING EVIDENCE
# =========================================================

print("\nTEST 6 : REPEATED SUPPORTING EVIDENCE")

confidence = 0.50

for _ in range(3):
    confidence = calibrate_confidence(
        current_confidence=confidence,
        conflict=False,
    )

print("Initial confidence :", 0.50)
print("After 3 supports   :", confidence)

assert abs(confidence - 0.80) < 1e-9

print("Repeated supporting evidence increases confidence: PASS")


# =========================================================
# TEST 7 : REPEATED CONTRADICTING EVIDENCE
# =========================================================

print("\nTEST 7 : REPEATED CONTRADICTING EVIDENCE")

confidence = 0.50

for _ in range(3):
    confidence = calibrate_confidence(
        current_confidence=confidence,
        conflict=True,
    )

print("Initial confidence :", 0.50)
print("After 3 conflicts  :", confidence)

assert abs(confidence - 0.20) < 1e-9

print("Repeated contradicting evidence decreases confidence: PASS")


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n==============================")
print("FINAL TEST SUMMARY")
print("==============================")

print("All confidence calibration tests: PASS")

