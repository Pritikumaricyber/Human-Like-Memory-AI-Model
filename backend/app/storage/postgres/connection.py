import psycopg2


DB_CONFIG = {
    "dbname": "human_memory",
    "user": "postgres",
    "password": "Priti@3204",
    "host": "localhost",
    "port": "5432",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)