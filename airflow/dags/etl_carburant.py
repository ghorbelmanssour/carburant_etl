from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from extract.download_data import download_xml
from transform.transform_data import transform_xml
from load.load_to_postgres import load_to_db
from load.create_etl_log_table import create_etl_log_table
from datetime import timedelta


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "execution_timeout": timedelta(minutes=5),
}

with DAG(
    dag_id="carburant_etl_dag",
    default_args=default_args,
    schedule_interval='*/10 * * * *',
    catchup=False,
    description="ETL complet des prix de carburants en France",
    tags=["ETL", "carburant"]
) as dag:

    init_db = PythonOperator(
        task_id='init_db',
        python_callable=create_etl_log_table,
        provide_context=True,
        dag=dag
    )

    extract = PythonOperator(
        task_id="extract_data",
        python_callable=download_xml,
        provide_context=True,
        dag=dag
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_xml,
        provide_context=True,
        dag=dag
    )

    load = PythonOperator(
        task_id="load_data",
        python_callable=load_to_db,
        provide_context=True,
        dag=dag
    )

    init_db >> extract >> transform >> load
