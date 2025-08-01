# ⛽ Carburant ETL – Pipeline de traitement des prix des carburants en France

Un pipeline **ETL local modulaire**, développé en Python, orchestré avec **Airflow** et stocké dans **PostgreSQL**, pour extraire, transformer et charger les données de prix de carburants en France publiées par le gouvernement (open data).

---

## 🚀 Objectifs

- Extraire les données XML compressées depuis l’API publique [roulez-eco.fr](https://donnees.roulez-eco.fr/opendata/instantane)
- Décompresser, parser et transformer les données avec pandas
- Charger dans une base PostgreSQL locale
- Orchestrer le tout avec Apache Airflow (Docker)
- Exporter les données en **CSV**
- Exporter les données en **Parquet** avec une structure type **Data Lake (bronze)**
- Centraliser les paramètres dans un fichier `.env`
- Visualiser les données avec Streamlit

---

## 🧰 Stack technique

- Python 3.12
- Apache Airflow 2.9 (via Docker)
- PostgreSQL 15
- pandas
- psycopg2
- pyarrow
- dotenv
- Docker / docker-compose
- Streamlit

---

## ⚙️ Installation et lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/<TON-UTILISATEUR>/carburant_etl.git
cd carburant_etl
```

### 2. Créer les dossiers de travail

```bash
mkdir -p airflow/data airflow/logs airflow/plugins
mkdir -p airflow/data/parquet/bronze
```

### 3. Créer le fichier `.env`

```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=airflow
DB_USER=airflow
DB_PASSWORD=airflow

RAW_DATA_PATH=/opt/airflow/data/PrixCarburants_instantane.xml
CLEAN_DATA_PATH=/opt/airflow/data/clean.csv
PARQUET_BRONZE_DIR=/opt/airflow/data/parquet/bronze
DATA_DIR=/opt/airflow/data
```

### 4. Démarrer les services avec Docker

```bash
docker-compose up --build
```

### 5. Accéder aux interfaces

- **Airflow** : [http://localhost:8080](http://localhost:8080) (`admin` / `admin`)
- **Streamlit** : [http://localhost:8501](http://localhost:8501)

---

## 📊 Données utilisées

- Source : [data.gouv.fr – prix des carburants](https://www.data.gouv.fr/fr/datasets/prix-des-carburants-en-france-flux-instantane)
- Format : XML compressé `.zip`
- Champs : nom station, ville, code postal, carburant, prix, date de mise à jour

---

## 🧪 Qualité des données

- Suppression des lignes avec `prix <= 0` ou valeurs manquantes
- Parsing strict des dates et types numériques
- Historisation des données Parquet dans un dossier daté (ex: /data/parquet/bronze/2025-08-01_20-45.parquet)
---

## 🔄 DAG Airflow

Le pipeline Airflow est composé de 4 tâches :

1. `extract_data` – Télécharge et décompresse les données XML
2. `transform_data` – Nettoie les données et les sauvegarde en CSV et Parquet
3. `load_data` – Charge les données dans PostgreSQL (depuis CSV et Parquet)

Planifié toutes les **10 minutes** (`*/10 * * * *`).

---

## 👨‍💻 Auteur

**Mohamed Manssour Ghorbel**  
Projet personnel de formation en data engineering  
📫 [LinkedIn](https://www.linkedin.com/in/mohamed-manssour-ghorbel-a93a8813b/)

---

## 📄 Licence

Ce projet est sous licence MIT – libre d’utilisation à des fins pédagogiques.
