import pandas as pd
import psycopg2
from config.config import DB_CONFIG, CLEAN_DATA_PATH

def load_to_db():
    df = pd.read_csv(CLEAN_DATA_PATH)

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prix_carburants (
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
        cursor.execute("""
            INSERT INTO prix_carburants (
                station_id, latitude, longitude, code_postal,
                ville, carburant, prix, date_maj
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row["station_id"], row["latitude"], row["longitude"],
            row["code_postal"], row["ville"], row["carburant"],
            row["prix"], row["date_maj"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Données chargées dans PostgreSQL")
