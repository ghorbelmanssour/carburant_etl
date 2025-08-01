import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

# Base de données
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# Chemins de fichiers
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")
CLEAN_DATA_PATH = os.getenv("CLEAN_DATA_PATH")
DATA_DIR = os.getenv("DATA_DIR")
PARQUET_BRONZE_DIR = os.getenv("PARQUET_BRONZE_DIR")
