import pandas as pd
import psycopg2
import os
from datetime import datetime
from config.config import DB_CONFIG, CLEAN_DATA_PATH, PARQUET_BRONZE_DIR
from config.log_utils import log_etl_event


def load_dataframe_to_postgres(df, table_name, cursor):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            station_id TEXT,
            latitude TEXT,
            longitude TEXT,
            code_postal TEXT,
            ville TEXT,
            carburant TEXT,
            prix FLOAT,
            date_maj TIMESTAMP
        )
    """)

    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT INTO {table_name} (
                station_id, latitude, longitude, code_postal,
                ville, carburant, prix, date_maj
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row["station_id"], row["latitude"], row["longitude"],
            row["code_postal"], row["ville"], row["carburant"],
            row["prix"], row["date_maj"]
        ))


def load_to_db(**context):
    execution_time = context["data_interval_start"]

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1. Charger CSV
        if os.path.exists(CLEAN_DATA_PATH):
            df_csv = pd.read_csv(CLEAN_DATA_PATH)
            load_dataframe_to_postgres(df_csv, "prix_carburants", cursor)
            print("✅ Données CSV chargées dans PostgreSQL")
        else:
            print("⚠️ Fichier CSV non trouvé")

        # 2. Charger Parquet daté
        date_str = datetime.now().strftime("%Y-%m-%d")
        parquet_path = os.path.join(PARQUET_BRONZE_DIR, f"{date_str}.parquet")

        if os.path.exists(parquet_path):
            df_parquet = pd.read_parquet(parquet_path)
            load_dataframe_to_postgres(df_parquet, "prix_carburants_parquet", cursor)
            print("✅ Données Parquet chargées dans PostgreSQL")
        else:
            print("⚠️ Fichier Parquet non trouvé")

        conn.commit()
        cursor.close()
        conn.close()
        log_etl_event("load_data", "SUCCESS", "CSV et Parquet chargés", execution_time)

    except Exception as e:
        log_etl_event("load_data", "FAILED", str(e), execution_time)
        raise
