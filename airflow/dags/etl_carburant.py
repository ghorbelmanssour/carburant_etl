from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from extract.download_data import download_xml
from transform.transform_data import transform_xml
from load.load_to_postgres import load_to_db

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

with DAG(
    dag_id="carburant_etl_dag",
    default_args=default_args,
    schedule_interval='*/10 * * * *',
    catchup=False,
    description="ETL complet des prix de carburants en France",
    tags=["ETL", "carburant"]
) as dag:

    extract = PythonOperator(
        task_id="extract_data",
        python_callable=download_xml
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_xml
    )

    load = PythonOperator(
        task_id="load_data",
        python_callable=load_to_db
    )

    extract >> transform >> load
