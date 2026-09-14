from backend.app.storage.postgres.connection import get_connection


EXPECTED_TABLES = {
    "memories",
    "beliefs",
    "evidence",
    "belief_history",
}


def test_database():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN (
                'memories',
                'beliefs',
                'evidence',
                'belief_history'
            )
            ORDER BY table_name;
            """
        )

        tables = {
            row[0]
            for row in cursor.fetchall()
        }

        print("Database connection: PASS")
        print("Tables found:")

        for table in sorted(tables):
            print(f"  - {table}")

        if tables == EXPECTED_TABLES:
            print("Database schema verification: PASS")
        else:
            missing = EXPECTED_TABLES - tables

            if missing:
                print(
                    "Missing tables:",
                    ", ".join(sorted(missing))
                )

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    test_database()