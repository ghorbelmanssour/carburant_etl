import psycopg2
from config.config import DB_CONFIG

def create_etl_log_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS etl_logs (
            id SERIAL PRIMARY KEY,
            task_name TEXT NOT NULL,
            status TEXT NOT NULL,
            execution_time TIMESTAMP DEFAULT NOW(),
            message TEXT
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Table etl_logs vérifiée/créée")
