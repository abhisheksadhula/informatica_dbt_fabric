FROM apache/airflow:2.9.3-python3.12

USER root

# Install system + ODBC dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/12/prod.list \
       > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean

USER airflow

# Install dbt
RUN pip install --no-cache-dir \
    dbt-core==1.11.2 \
    dbt-fabric==1.9.8

ENV PATH="/home/airflow/.local/bin:${PATH}"
