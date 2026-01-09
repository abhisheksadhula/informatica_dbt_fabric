from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

DBT_DIR = "/opt/airflow/dbt"

with DAG(
    dag_id="dbt_fabric_pipeline",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["dbt", "fabric"],
) as dag:

    source_freshness = BashOperator(
        task_id="dbt_source_freshness",
        bash_command=f"cd {DBT_DIR} && dbt source freshness",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && dbt test",
    )

    source_freshness >> dbt_run >> dbt_test
