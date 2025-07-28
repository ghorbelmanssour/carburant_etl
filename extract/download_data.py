import requests
import zipfile
import io
import os

def download_xml():
    url = "https://donnees.roulez-eco.fr/opendata/instantane"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    os.makedirs("/opt/airflow/data", exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall("/opt/airflow/data/")
        print("✅ Fichier XML extrait dans /opt/airflow/data/")
