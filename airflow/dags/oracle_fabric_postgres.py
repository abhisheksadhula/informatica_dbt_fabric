import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
from datetime import datetime, timedelta
import requests
import msal
import base64
import json
import time
import os

# ---------------------------
# Airflow Variables
# ---------------------------
FABRIC_TENANT_ID = "<YOUR_TENANT_ID>"
FABRIC_CLIENT_ID = "<YOUR_CLIENT_ID>"
FABRIC_CLIENT_SECRET= "<YOUR_CLIENT_SECRET>"
FABRIC_WORKSPACE_ID= "<YOUR_WORKSPACE_ID>"
FABRIC_PIPELINE_ID= "<YOUR_PIPELINE_ID>"
AUTHORITY = f"https://login.microsoftonline.com/{FABRIC_TENANT_ID}"
SCOPE = ["https://api.fabric.microsoft.com/.default"]

# ---------------------------
# Token Generation
# ---------------------------
def get_fabric_token():
    app = msal.ConfidentialClientApplication(
        FABRIC_CLIENT_ID,
        authority=AUTHORITY,
        client_credential=FABRIC_CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=SCOPE)

    if "access_token" not in result:
        raise AirflowFailException(result)

    return result["access_token"]

# ---------------------------
# Trigger Fabric Pipeline
# ---------------------------
def trigger_pipeline(ti):
    token = get_fabric_token()

    url = (
        f"https://api.fabric.microsoft.com/v1/workspaces/"
        f"{FABRIC_WORKSPACE_ID}/items/{FABRIC_PIPELINE_ID}/jobs/instances"
        f"?jobType=Pipeline"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code != 202:
        raise AirflowFailException(response.text)

    job_id = (
        response.headers.get("x-ms-job-id")
        or response.headers.get("x-ms-job-instance-id")
    )

    if not job_id:
        location = response.headers.get("Location")
        if location:
            job_id = location.split("/")[-1]

    if not job_id:
        raise AirflowFailException("No job id returned from Fabric")

    ti.xcom_push(key="job_id", value=job_id)

# ---------------------------
# Poll Pipeline Status
# ---------------------------
def poll_status(ti):
    token = get_fabric_token()
    job_id = ti.xcom_pull(key="job_id", task_ids="trigger_pipeline")

    url = (
        f"https://api.fabric.microsoft.com/v1/workspaces/"
        f"{FABRIC_WORKSPACE_ID}/items/{FABRIC_PIPELINE_ID}/jobs/instances/{job_id}"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        status = response.json()["status"]

        print("Pipeline status:", status)

        if status in ["Completed", "Succeeded"]:
            return

        if status in ["Failed", "Cancelled"]:
            raise AirflowFailException("Fabric pipeline failed")

        time.sleep(30)

# ---------------------------
# DAG Definition
# ---------------------------
with DAG(
    dag_id="fabric_pipeline_orchestration",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=5)
    }
) as dag:

    trigger = PythonOperator(
        task_id="trigger_pipeline",
        python_callable=trigger_pipeline
    )

    poll = PythonOperator(
        task_id="poll_pipeline_status",
        python_callable=poll_status
    )

    trigger >> poll
