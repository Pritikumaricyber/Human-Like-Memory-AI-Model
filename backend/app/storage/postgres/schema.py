from backend.app.storage.postgres.connection import get_connection


def create_tables():
    """
    Create all PostgreSQL tables required by the
    Human-Like Memory Architecture.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # =====================================================
        # 1. MEMORIES
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,

                content TEXT NOT NULL,
                memory_type VARCHAR(50) NOT NULL DEFAULT 'fact',

                importance DOUBLE PRECISION NOT NULL DEFAULT 0.5
                    CHECK (importance >= 0.0 AND importance <= 1.0),

                emotional_score DOUBLE PRECISION NOT NULL DEFAULT 0.0
                    CHECK (emotional_score >= 0.0 AND emotional_score <= 1.0),

                confidence DOUBLE PRECISION NOT NULL DEFAULT 0.5
                    CHECK (confidence >= 0.0 AND confidence <= 1.0),

                frequency INTEGER NOT NULL DEFAULT 0
                    CHECK (frequency >= 0),

                strength DOUBLE PRECISION NOT NULL DEFAULT 0.5
                    CHECK (strength >= 0.0 AND strength <= 1.0),

                decay_rate DOUBLE PRECISION NOT NULL DEFAULT 0.01
                    CHECK (decay_rate >= 0.0 AND decay_rate <= 1.0),

                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_recalled TIMESTAMP NULL,

                topics TEXT[] NOT NULL DEFAULT '{}',
                entities TEXT[] NOT NULL DEFAULT '{}',
                related_memories TEXT[] NOT NULL DEFAULT '{}',

                status VARCHAR(50) NOT NULL DEFAULT 'active',

                embedding DOUBLE PRECISION[] NULL,

                recall_count INTEGER NOT NULL DEFAULT 0
                    CHECK (recall_count >= 0),

                belief_id VARCHAR(36) NULL
            );
            """
        )

        # =====================================================
        # 2. BELIEFS
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS beliefs (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,

                subject VARCHAR(255) NOT NULL,
                belief TEXT NOT NULL,

                confidence DOUBLE PRECISION NOT NULL DEFAULT 0.5
                    CHECK (confidence >= 0.0 AND confidence <= 1.0),

                currentness DOUBLE PRECISION NOT NULL DEFAULT 1.0
                    CHECK (currentness >= 0.0 AND currentness <= 1.0),

                state VARCHAR(50) NOT NULL DEFAULT 'new'
                    CHECK (
                        state IN (
                            'new',
                            'supported',
                            'weakened',
                            'contested',
                            'superseded'
                        )
                    ),

                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # =====================================================
        # 3. EVIDENCE
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS evidence (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,

                belief_id VARCHAR(36) NULL,

                content TEXT NOT NULL,

                evidence_type VARCHAR(50) NOT NULL
                    CHECK (
                        evidence_type IN (
                            'statement',
                            'behavior',
                            'event',
                            'inference'
                        )
                    ),

                relationship VARCHAR(50) NOT NULL
                    CHECK (
                        relationship IN (
                            'support',
                            'contradict',
                            'refinement',
                            'duplicate',
                            'context',
                            'unrelated'
                        )
                    ),

                reliability DOUBLE PRECISION NOT NULL DEFAULT 0.5
                    CHECK (reliability >= 0.0 AND reliability <= 1.0),

                specificity DOUBLE PRECISION NOT NULL DEFAULT 0.5
                    CHECK (specificity >= 0.0 AND specificity <= 1.0),

                independence DOUBLE PRECISION NOT NULL DEFAULT 1.0
                    CHECK (independence >= 0.0 AND independence <= 1.0),

                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # =====================================================
        # 4. BELIEF HISTORY
        # =====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS belief_history (
                id VARCHAR(36) PRIMARY KEY,

                belief_id VARCHAR(36) NOT NULL,
                evidence_id VARCHAR(36) NULL,

                previous_confidence DOUBLE PRECISION NOT NULL
                    CHECK (
                        previous_confidence >= 0.0
                        AND previous_confidence <= 1.0
                    ),

                new_confidence DOUBLE PRECISION NOT NULL
                    CHECK (
                        new_confidence >= 0.0
                        AND new_confidence <= 1.0
                    ),

                previous_currentness DOUBLE PRECISION NOT NULL
                    CHECK (
                        previous_currentness >= 0.0
                        AND previous_currentness <= 1.0
                    ),

                new_currentness DOUBLE PRECISION NOT NULL
                    CHECK (
                        new_currentness >= 0.0
                        AND new_currentness <= 1.0
                    ),

                previous_state VARCHAR(50) NOT NULL,
                new_state VARCHAR(50) NOT NULL,

                change_type VARCHAR(50) NOT NULL,

                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # =====================================================
        # INDEXES
        # =====================================================

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_memories_user_id
            ON memories(user_id);
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_memories_status
            ON memories(status);
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_beliefs_user_id
            ON beliefs(user_id);
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_evidence_belief_id
            ON evidence(belief_id);
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_history_belief_id
            ON belief_history(belief_id);
            """
        )

        connection.commit()

        print("PostgreSQL tables created successfully!")

    except Exception as e:

        connection.rollback()

        print("Failed to create PostgreSQL tables:")
        print(e)

        raise

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_tables()