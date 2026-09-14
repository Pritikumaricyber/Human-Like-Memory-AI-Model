from backend.app.models.evidence import Evidence
from backend.app.storage.postgres.connection import get_connection


class PostgresEvidenceStore:
    """
    PostgreSQL-backed persistent storage for Evidence objects.
    """

    # =========================================================
    # ADD
    # =========================================================

    def add(self, evidence: Evidence) -> None:
        """
        Store a new evidence record.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO evidence (
                    id,
                    user_id,
                    belief_id,
                    content,
                    evidence_type,
                    relationship,
                    reliability,
                    specificity,
                    independence,
                    created_at
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    evidence.id,
                    evidence.user_id,
                    evidence.belief_id,
                    evidence.content,
                    evidence.evidence_type,
                    evidence.relationship,
                    evidence.reliability,
                    evidence.specificity,
                    evidence.independence,
                    evidence.created_at,
                ),
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ALL
    # =========================================================

    def get_all(self) -> list[Evidence]:
        """
        Return all evidence records.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    belief_id,
                    content,
                    evidence_type,
                    relationship,
                    reliability,
                    specificity,
                    independence,
                    created_at
                FROM evidence
                ORDER BY created_at ASC
                """
            )

            rows = cursor.fetchall()

            return [
                self._row_to_evidence(row)
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(
        self,
        evidence_id: str,
    ) -> Evidence | None:
        """
        Find evidence by ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    belief_id,
                    content,
                    evidence_type,
                    relationship,
                    reliability,
                    specificity,
                    independence,
                    created_at
                FROM evidence
                WHERE id = %s
                """,
                (evidence_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_evidence(row)

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # FIND BY BELIEF
    # =========================================================

    def find_by_belief(
        self,
        belief_id: str,
    ) -> list[Evidence]:
        """
        Return all evidence associated with a belief.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    belief_id,
                    content,
                    evidence_type,
                    relationship,
                    reliability,
                    specificity,
                    independence,
                    created_at
                FROM evidence
                WHERE belief_id = %s
                ORDER BY created_at ASC
                """,
                (belief_id,),
            )

            rows = cursor.fetchall()

            return [
                self._row_to_evidence(row)
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # FIND BY USER
    # =========================================================

    def find_by_user(
        self,
        user_id: str,
    ) -> list[Evidence]:
        """
        Return all evidence belonging to a user.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    belief_id,
                    content,
                    evidence_type,
                    relationship,
                    reliability,
                    specificity,
                    independence,
                    created_at
                FROM evidence
                WHERE user_id = %s
                ORDER BY created_at ASC
                """,
                (user_id,),
            )

            rows = cursor.fetchall()

            return [
                self._row_to_evidence(row)
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        evidence: Evidence,
    ) -> bool:
        """
        Update an existing evidence record.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE evidence
                SET
                    user_id = %s,
                    belief_id = %s,
                    content = %s,
                    evidence_type = %s,
                    relationship = %s,
                    reliability = %s,
                    specificity = %s,
                    independence = %s,
                    created_at = %s
                WHERE id = %s
                """,
                (
                    evidence.user_id,
                    evidence.belief_id,
                    evidence.content,
                    evidence.evidence_type,
                    evidence.relationship,
                    evidence.reliability,
                    evidence.specificity,
                    evidence.independence,
                    evidence.created_at,
                    evidence.id,
                ),
            )

            connection.commit()

            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        evidence_id: str,
    ) -> bool:
        """
        Delete evidence by ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM evidence
                WHERE id = %s
                """,
                (evidence_id,),
            )

            connection.commit()

            return cursor.rowcount > 0

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # COUNT
    # =========================================================

    def count(self) -> int:
        """
        Return the total number of evidence records.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM evidence
                """
            )

            return cursor.fetchone()[0]

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:
        """
        Delete all evidence records.

        Primarily useful for testing.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM evidence
                """
            )

            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # ROW → EVIDENCE
    # =========================================================

    @staticmethod
    def _row_to_evidence(row) -> Evidence:
        """
        Convert a PostgreSQL row into an Evidence object.
        """

        return Evidence(
            id=row[0],
            user_id=row[1],
            belief_id=row[2],
            content=row[3],
            evidence_type=row[4],
            relationship=row[5],
            reliability=row[6],
            specificity=row[7],
            independence=row[8],
            created_at=row[9],
        )