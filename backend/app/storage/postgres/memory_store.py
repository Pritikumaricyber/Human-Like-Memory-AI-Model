from backend.app.models.memory import Memory
from backend.app.storage.postgres.connection import get_connection


class PostgresMemoryStore:
    """
    PostgreSQL-backed persistent storage for Memory objects.

    This store provides the same basic operations needed by
    the existing MemoryManager while storing memories permanently
    in PostgreSQL.
    """

    # =========================================================
    # ADD
    # =========================================================

    def add(self, memory: Memory) -> None:
        """
        Store a new memory in PostgreSQL.

        Exact duplicate memories for the same user are ignored.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            # -------------------------------------------------
            # Prevent exact duplicate memories
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT id
                FROM memories
                WHERE user_id = %s
                  AND content = %s
                LIMIT 1
                """,
                (
                    memory.user_id,
                    memory.content,
                ),
            )

            existing = cursor.fetchone()

            if existing is not None:
                print(
                    f"Duplicate memory ignored: "
                    f"{memory.content}"
                )
                return

            # -------------------------------------------------
            # Insert new memory
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO memories (
                    id,
                    user_id,
                    content,
                    memory_type,
                    importance,
                    emotional_score,
                    confidence,
                    frequency,
                    strength,
                    decay_rate,
                    created_at,
                    last_recalled,
                    topics,
                    entities,
                    related_memories,
                    status,
                    embedding,
                    recall_count,
                    belief_id
                )
                VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    memory.id,
                    memory.user_id,
                    memory.content,
                    memory.memory_type,
                    memory.importance,
                    memory.emotional_score,
                    memory.confidence,
                    memory.frequency,
                    memory.strength,
                    memory.decay_rate,
                    memory.created_at,
                    memory.last_recalled,
                    memory.topics,
                    memory.entities,
                    memory.related_memories,
                    memory.status,
                    memory.embedding,
                    memory.recall_count,
                    memory.belief_id,
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

    def get_all(self) -> list[Memory]:
        """
        Return all memories from PostgreSQL.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    content,
                    memory_type,
                    importance,
                    emotional_score,
                    confidence,
                    frequency,
                    strength,
                    decay_rate,
                    created_at,
                    last_recalled,
                    topics,
                    entities,
                    related_memories,
                    status,
                    embedding,
                    recall_count,
                    belief_id
                FROM memories
                ORDER BY created_at ASC
                """
            )

            rows = cursor.fetchall()

            return [
                self._row_to_memory(row)
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
        memory_id: str,
    ) -> Memory | None:
        """
        Find a memory by ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    content,
                    memory_type,
                    importance,
                    emotional_score,
                    confidence,
                    frequency,
                    strength,
                    decay_rate,
                    created_at,
                    last_recalled,
                    topics,
                    entities,
                    related_memories,
                    status,
                    embedding,
                    recall_count,
                    belief_id
                FROM memories
                WHERE id = %s
                """,
                (memory_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_memory(row)

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        memory: Memory,
    ) -> bool:
        """
        Update an existing memory.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE memories
                SET
                    user_id = %s,
                    content = %s,
                    memory_type = %s,
                    importance = %s,
                    emotional_score = %s,
                    confidence = %s,
                    frequency = %s,
                    strength = %s,
                    decay_rate = %s,
                    created_at = %s,
                    last_recalled = %s,
                    topics = %s,
                    entities = %s,
                    related_memories = %s,
                    status = %s,
                    embedding = %s,
                    recall_count = %s,
                    belief_id = %s
                WHERE id = %s
                """,
                (
                    memory.user_id,
                    memory.content,
                    memory.memory_type,
                    memory.importance,
                    memory.emotional_score,
                    memory.confidence,
                    memory.frequency,
                    memory.strength,
                    memory.decay_rate,
                    memory.created_at,
                    memory.last_recalled,
                    memory.topics,
                    memory.entities,
                    memory.related_memories,
                    memory.status,
                    memory.embedding,
                    memory.recall_count,
                    memory.belief_id,
                    memory.id,
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
        memory_id: str,
    ) -> bool:
        """
        Delete a memory by ID.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM memories
                WHERE id = %s
                """,
                (memory_id,),
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
        Return the number of stored memories.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM memories
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
        Delete all memories.

        This is primarily useful for testing.
        """

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM memories
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
    # ROW → MEMORY
    # =========================================================

    @staticmethod
    def _row_to_memory(
        row,
    ) -> Memory:
        """
        Convert a PostgreSQL row into a Memory object.
        """

        return Memory(
            id=row[0],
            user_id=row[1],
            content=row[2],
            memory_type=row[3],
            importance=row[4],
            emotional_score=row[5],
            confidence=row[6],
            frequency=row[7],
            strength=row[8],
            decay_rate=row[9],
            created_at=row[10],
            last_recalled=row[11],
            topics=row[12] or [],
            entities=row[13] or [],
            related_memories=row[14] or [],
            status=row[15],
            embedding=row[16],
            recall_count=row[17],
            belief_id=row[18],
        )