import psycopg2
from datetime import datetime
from config.config import DB_CONFIG

def log_etl_event(task_name, status, message="", execution_time=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO etl_logs (task_name, status, execution_time, message)
            VALUES (%s, %s, %s, %s)
        """, (
            task_name,
            status,
            (execution_time or datetime.now()).replace(tzinfo=None),
            message
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"📌 Log enregistré : {task_name} - {status}")
    except Exception as e:
        print(f"❌ Échec lors de l’enregistrement du log : {e}")
