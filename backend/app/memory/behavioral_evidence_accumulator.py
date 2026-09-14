class BehavioralEvidenceAccumulator:
    """
    Accumulates behavioral observations while preventing
    exact duplicate observations from being counted twice.
    """

    def __init__(self):
        self._evidence = []

    def add(self, evidence: dict) -> bool:
        """
        Add behavioral evidence.

        If the evidence explicitly represents a preference change,
        mark the previous preference as superseded while preserving
        the historical observation.
        Returns:
             True  -> evidence was added
             False -> exact duplicate was ignored
        """

        if self._is_duplicate(evidence):
            return False

        preference_change = evidence.get("preference_change")

        if preference_change is not None:
            self._mark_superseded_preference(
                user_id=evidence.get("user_id"),
                superseded_concept=preference_change.get(
                    "superseded_preference"
                ),
        )

        self._evidence.append(evidence)
        return True

    def _mark_superseded_preference(
            self,
            user_id: str | None,
            superseded_concept: str | None,
            ) -> None:
        """
        Mark a previous preference as superseded.

        Historical evidence is retained rather than deleted.
        """
        if user_id is None or superseded_concept is None:
            return
        for existing in self._evidence:
            if (
                existing.get("user_id") == user_id
                and existing.get("concept") == superseded_concept
                and existing.get("behavior") == "preference"
                and existing.get("direction") == "positive"
            ):
                existing["superseded"] = True
                existing["superseded_by"] = "preference_change"

    def _is_duplicate(self, evidence: dict) -> bool:
        for existing in self._evidence:
            if (
                existing.get("user_id") == evidence.get("user_id")
                and existing.get("concept") == evidence.get("concept")
                and existing.get("behavior") == evidence.get("behavior")
                and existing.get("direction") == evidence.get("direction")
                and existing.get("source_text") == evidence.get("source_text")
            ):
                return True

        return False

    def get_all(self) -> list[dict]:
        """
        Return all accumulated behavioral observations.
        """
        return list(self._evidence)

    def get_by_concept(
        self,
        concept: str,
        user_id: str | None = None,
    ) -> list[dict]:
        """
        Return behavioral observations for one concept.

        If user_id is provided, only observations belonging
        to that user are returned.
        """

        return [
            evidence
            for evidence in self._evidence
            if (
                evidence.get("concept") == concept
                and (
                    user_id is None
                    or evidence.get("user_id") == user_id
                )
            )
        ]

    def count(self) -> int:
        """
        Return total number of accumulated observations.
        """
        return len(self._evidence)

    def count_by_concept(
        self,
        concept: str,
        user_id: str | None = None,
    ) -> int:
        """
        Return number of observations for one concept.
        """
        return len(
            self.get_by_concept(
                concept,
                user_id=user_id,
            )
        )