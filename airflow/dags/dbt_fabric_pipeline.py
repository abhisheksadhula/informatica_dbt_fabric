from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.models import Variable

DBT_DIR = "/opt/airflow/dbt"

default_args = {
    "owner": "data-eng",
    "retries": 0,
}

with DAG(
    dag_id="dbt_fabric_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=f"cd {DBT_DIR} && dbt deps",
    )

    source_freshness = BashOperator(
        task_id="dbt_source_freshness",
        bash_command=f"cd {DBT_DIR} && dbt source freshness"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test"
    )

    dbt_deps >> source_freshness >> dbt_run >> dbt_test
