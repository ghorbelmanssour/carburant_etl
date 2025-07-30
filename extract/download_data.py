import requests
import zipfile
import io
import os
from config.config import DATA_DIR, RAW_DATA_PATH

def download_xml():
    url = "https://donnees.roulez-eco.fr/opendata/instantane"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    os.makedirs(DATA_DIR, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(DATA_DIR)
        print("✅ Fichier XML extrait dans {DATA_DIR}")
