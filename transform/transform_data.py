import xml.etree.ElementTree as ET
import pandas as pd
import os
from config.config import RAW_DATA_PATH, CLEAN_DATA_PATH, PARQUET_BRONZE_DIR
from config.log_utils import log_etl_event
from datetime import datetime


def transform_xml(**context):
    execution_time = context["data_interval_start"]

    try:
        tree = ET.parse(RAW_DATA_PATH)
        root = tree.getroot()

        rows = []
        for pdv in root.findall("pdv"):
            station_id = pdv.attrib.get("id")
            lat = pdv.attrib.get("latitude")
            lon = pdv.attrib.get("longitude")
            cp = pdv.attrib.get("cp")
            ville = pdv.findtext("ville", default="Inconnu")

            for prix in pdv.findall("prix"):
                carburant = prix.attrib.get("nom")
                valeur = prix.attrib.get("valeur")
                date = prix.attrib.get("maj")

                rows.append({
                    "station_id": station_id,
                    "latitude": lat,
                    "longitude": lon,
                    "code_postal": cp,
                    "ville": ville,
                    "carburant": carburant,
                    "prix": float(valeur) / 100,
                    "date_maj": date
                })

        df = pd.DataFrame(rows)
        df.dropna(subset=["prix"], inplace=True)
        df = df[df["prix"] > 0]
        df["date_maj"] = pd.to_datetime(df["date_maj"])

        df.to_csv(CLEAN_DATA_PATH, index=False)
        print("Données transformées sauvegardées dans", CLEAN_DATA_PATH)

        os.makedirs(PARQUET_BRONZE_DIR, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
        parquet_path = os.path.join(PARQUET_BRONZE_DIR, f"{date_str}.parquet")

        df.to_parquet(parquet_path, index=False)
        print(f"Données sauvegardées au format Parquet dans {parquet_path}")
            
        log_etl_event("transform_data", "SUCCESS", "Transformation OK", execution_time)

    except Exception as e:
        log_etl_event("transform_data", "FAILED", str(e), execution_time)
        raise
