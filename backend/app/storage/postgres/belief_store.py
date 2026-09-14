from backend.app.models.belief import Belief
from backend.app.storage.postgres.connection import get_connection


class PostgresBeliefStore:
    """
    PostgreSQL-backed persistent storage for Belief objects.
    """

    # =========================================================
    # ADD
    # =========================================================

    def add(self, belief: Belief) -> None:
        """
        Store a new belief in PostgreSQL.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO beliefs (
                    id,
                    user_id,
                    subject,
                    belief,
                    confidence,
                    currentness,
                    state,
                    created_at,
                    updated_at
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                """,
                (
                    belief.id,
                    belief.user_id,
                    belief.subject,
                    belief.belief,
                    belief.confidence,
                    belief.currentness,
                    belief.state,
                    belief.created_at,
                    belief.updated_at,
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

    def get_all(self) -> list[Belief]:
        """
        Return all beliefs from PostgreSQL.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    subject,
                    belief,
                    confidence,
                    currentness,
                    state,
                    created_at,
                    updated_at
                FROM beliefs
                ORDER BY created_at ASC
                """
            )

            rows = cursor.fetchall()

            return [
                self._row_to_belief(row)
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
        belief_id: str,
    ) -> Belief | None:
        """
        Find a belief by ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    subject,
                    belief,
                    confidence,
                    currentness,
                    state,
                    created_at,
                    updated_at
                FROM beliefs
                WHERE id = %s
                """,
                (belief_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_belief(row)

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # FIND BY SUBJECT
    # =========================================================

    def find_by_subject(
        self,
        subject: str,
    ) -> Belief | None:
        """
        Find a belief by subject.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    subject,
                    belief,
                    confidence,
                    currentness,
                    state,
                    created_at,
                    updated_at
                FROM beliefs
                WHERE LOWER(subject) = LOWER(%s)
                LIMIT 1
                """,
                (subject,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_belief(row)

        finally:
            cursor.close()
            connection.close()

        # =========================================================
    # FIND SIMILAR BELIEF
    # =========================================================

    def find_similar_belief(
        self,
        belief_text: str,
        user_id: str,
        threshold: float = 0.70,
    ) -> tuple[Belief | None, float]:
        """
        Find the most semantically similar belief
        belonging to the same user.
        """

        from backend.app.memory.belief_matcher import (
            calculate_belief_similarity,
        )

        best_belief = None
        best_similarity = 0.0

        for belief in self.get_all():

            if belief.user_id != user_id:
                continue

            similarity = calculate_belief_similarity(
                belief_text,
                belief.belief,
            )

            if similarity > best_similarity:
                best_similarity = similarity
                best_belief = belief

        if best_similarity >= threshold:
            return best_belief, best_similarity

        return None, best_similarity        

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        belief: Belief,
    ) -> bool:
        """
        Update an existing belief.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE beliefs
                SET
                    user_id = %s,
                    subject = %s,
                    belief = %s,
                    confidence = %s,
                    currentness = %s,
                    state = %s,
                    created_at = %s,
                    updated_at = %s
                WHERE id = %s
                """,
                (
                    belief.user_id,
                    belief.subject,
                    belief.belief,
                    belief.confidence,
                    belief.currentness,
                    belief.state,
                    belief.created_at,
                    belief.updated_at,
                    belief.id,
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
        belief_id: str,
    ) -> bool:
        """
        Delete a belief by ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM beliefs
                WHERE id = %s
                """,
                (belief_id,),
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
        Return the total number of beliefs.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM beliefs
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
        Delete all beliefs.

        Primarily useful for testing.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM beliefs
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
    # ROW → BELIEF
    # =========================================================

    @staticmethod
    def _row_to_belief(row) -> Belief:
        """
        Convert a PostgreSQL row into a Belief object.
        """

        return Belief(
            id=row[0],
            user_id=row[1],
            subject=row[2],
            belief=row[3],
            confidence=row[4],
            currentness=row[5],
            state=row[6],
            created_at=row[7],
            updated_at=row[8],
        )