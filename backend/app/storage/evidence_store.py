from backend.app.models.evidence import Evidence


class EvidenceStore:

    def __init__(self):
        self.evidence: list[Evidence] = []

    def add(self, evidence: Evidence):
        self.evidence.append(evidence)

    def get_all(self):
        return self.evidence

    def remove(self, evidence: Evidence):
        self.evidence.remove(evidence)