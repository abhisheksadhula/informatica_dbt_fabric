from airflow import DAG
from airflow.providers.oracle.hooks.oracle import OracleHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime

def oracle_to_postgres():

    oracle = OracleHook(oracle_conn_id="oracle_conn")
    postgres = PostgresHook(postgres_conn_id="postgres_conn")

    oracle_conn = oracle.get_conn()
    pg_conn = postgres.get_conn()

    oracle_cursor = oracle_conn.cursor()
    pg_cursor = pg_conn.cursor()

    oracle_cursor.execute("""
        SELECT id, first_name, last_name, created_date
        FROM customers
    """)

    rows = oracle_cursor.fetchall()

    insert_sql = """
        INSERT INTO raw_oracle.customers
        (id, first_name, last_name, created_date)
        VALUES (%s, %s, %s, %s)
    """

    pg_cursor.executemany(insert_sql, rows)

    pg_conn.commit()

    oracle_cursor.close()
    pg_cursor.close()

with DAG(
    dag_id="oracle_to_postgres_ingestion",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["oracle", "postgres", "ingestion"],
) as dag:

    ingest_oracle = PythonOperator(
        task_id="oracle_to_postgres",
        python_callable=oracle_to_postgres
    )

    ingest_oracle
