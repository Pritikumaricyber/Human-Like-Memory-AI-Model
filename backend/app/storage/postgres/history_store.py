from backend.app.models.belief_history import BeliefHistory
from backend.app.storage.postgres.connection import get_connection


class PostgresHistoryStore:
    """
    PostgreSQL-backed persistent storage for belief history.
    """

    # =========================================================
    # ADD
    # =========================================================

    def add(self, history: BeliefHistory) -> None:
        """
        Store a new belief history record.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO belief_history (
                    id,
                    belief_id,
                    evidence_id,
                    previous_confidence,
                    new_confidence,
                    previous_currentness,
                    new_currentness,
                    previous_state,
                    new_state,
                    change_type,
                    created_at
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    history.id,
                    history.belief_id,
                    history.evidence_id,
                    history.previous_confidence,
                    history.new_confidence,
                    history.previous_currentness,
                    history.new_currentness,
                    history.previous_state,
                    history.new_state,
                    history.change_type,
                    history.created_at,
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

    def get_all(self) -> list[BeliefHistory]:
        """
        Return all belief history records.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    belief_id,
                    evidence_id,
                    previous_confidence,
                    new_confidence,
                    previous_currentness,
                    new_currentness,
                    previous_state,
                    new_state,
                    change_type,
                    created_at
                FROM belief_history
                ORDER BY created_at ASC
                """
            )

            rows = cursor.fetchall()

            return [
                self._row_to_history(row)
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
        history_id: str,
    ) -> BeliefHistory | None:
        """
        Find a history record by ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    belief_id,
                    evidence_id,
                    previous_confidence,
                    new_confidence,
                    previous_currentness,
                    new_currentness,
                    previous_state,
                    new_state,
                    change_type,
                    created_at
                FROM belief_history
                WHERE id = %s
                """,
                (history_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_history(row)

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # FIND BY BELIEF
    # =========================================================

    def find_by_belief(
        self,
        belief_id: str,
    ) -> list[BeliefHistory]:
        """
        Return the complete history of a belief.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    belief_id,
                    evidence_id,
                    previous_confidence,
                    new_confidence,
                    previous_currentness,
                    new_currentness,
                    previous_state,
                    new_state,
                    change_type,
                    created_at
                FROM belief_history
                WHERE belief_id = %s
                ORDER BY created_at ASC
                """,
                (belief_id,),
            )

            rows = cursor.fetchall()

            return [
                self._row_to_history(row)
                for row in rows
            ]

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # COUNT
    # =========================================================

    def count(self) -> int:
        """
        Return the total number of history records.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM belief_history
                """
            )

            return cursor.fetchone()[0]

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        history_id: str,
    ) -> bool:
        """
        Delete a history record by ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM belief_history
                WHERE id = %s
                """,
                (history_id,),
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
    # CLEAR
    # =========================================================

    def clear(self) -> None:
        """
        Delete all history records.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM belief_history
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
    # ROW → MODEL
    # =========================================================

    @staticmethod
    def _row_to_history(row) -> BeliefHistory:
        """
        Convert a PostgreSQL row into a BeliefHistory object.
        """

        return BeliefHistory(
            id=row[0],
            belief_id=row[1],
            evidence_id=row[2],
            previous_confidence=row[3],
            new_confidence=row[4],
            previous_currentness=row[5],
            new_currentness=row[6],
            previous_state=row[7],
            new_state=row[8],
            change_type=row[9],
            created_at=row[10],
        )