import requests
import zipfile
import io
import os
from config.config import DATA_DIR, RAW_DATA_PATH
from config.log_utils import log_etl_event


def download_xml(**context):
    url = "https://donnees.roulez-eco.fr/opendata/instantane"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    execution_time = context["data_interval_start"]

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        os.makedirs(DATA_DIR, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(DATA_DIR)

        print(f"✅ Fichier XML extrait dans {DATA_DIR}")
        log_etl_event("extract_data", "SUCCESS", "Fichier téléchargé et extrait", execution_time)

    except Exception as e:
        log_etl_event("extract_data", "FAILED", str(e), execution_time)
        raise
