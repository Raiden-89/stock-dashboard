from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


def stampa_hello():
    print("✅ DAG di test funzionante!")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="dag_test_semplice",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
    tags=["test"],
) as dag:

    task_stampa = PythonOperator(
        task_id="stampa_hello",
        python_callable=stampa_hello
    )
