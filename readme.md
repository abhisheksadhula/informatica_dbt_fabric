# Informatica DBT Fabric Pipeline

A data engineering project that integrates Apache Airflow with dbt (Data Build Tool) to orchestrate and transform data stored in Microsoft Fabric.

## Project Overview

This project demonstrates a modern data pipeline architecture that combines:
- **Apache Airflow** for workflow orchestration and scheduling
- **dbt** for data transformation and modeling
- **Microsoft Fabric** as the data warehouse platform

The pipeline processes raw customer and order data through staging and mart layers, ensuring data quality and freshness.

## Project Structure

```
informatica_dbt_fabric/
├── airflow/                    # Airflow orchestration setup
│   ├── docker-compose.yml      # Docker Compose configuration for Airflow
│   ├── Dockerfile             # Custom Airflow Docker image
│   ├── dags/                  # Airflow DAGs
│   │   └── dbt_fabric_pipeline.py  # Main pipeline DAG
│   ├── logs/                  # Airflow execution logs
│   └── plugins/               # Custom Airflow plugins
├── dbt_fabric/               # dbt project directory
│   ├── dbt_project.yml       # dbt project configuration
│   ├── profiles.yml          # Database connection profiles
│   ├── packages.yml          # dbt package dependencies
│   ├── models/               # dbt data models
│   │   ├── sources/          # Source table definitions
│   │   ├── staging/          # Raw data cleaning layer
│   │   └── marts/            # Business-ready data marts
│   ├── seeds/                # Static data files
│   ├── snapshots/            # Slowly changing dimensions
│   ├── tests/                # Custom data tests
│   ├── macros/               # Reusable dbt macros
│   └── target/               # Compiled dbt artifacts
└── README.md                 # This file
```

## Architecture

### Data Flow
1. **Raw Data**: Customer and order data stored in Microsoft Fabric Warehouse (`raw` database)
2. **Staging Layer**: Basic data cleaning and type casting
3. **Mart Layer**: Business logic transformations and aggregations
4. **Quality Checks**: Automated testing and source freshness monitoring

### Technologies Used
- **Microsoft Fabric**: Cloud data warehouse
- **dbt**: Data transformation tool
- **Apache Airflow**: Workflow orchestration
- **Docker**: Containerization for Airflow
- **PostgreSQL**: Airflow metadata database

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Microsoft Fabric workspace with appropriate permissions
- Service Principal for Fabric authentication

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd informatica_dbt_fabric
   ```

2. **Configure Microsoft Fabric Connection**
   - Update `dbt_fabric/profiles.yml` with your Fabric credentials:
     - `tenant_id`: Your Azure tenant ID
     - `client_id`: Service principal client ID
     - `client_secret`: Service principal secret

3. **Start Docker Desktop**
   - Ensure Docker Desktop is running in Linux container mode 

3. **Start Airflow Environment**
   ```bash
   cd airflow
   docker compose build
   docker compose up airflow-init
   docker compose up
   ```

4. **Access Airflow UI**
   - Open http://localhost:8081
   - Username: `admin`
   - Password: `admin`

5. **Secrets & Configuration**
   - Microsoft Fabric credentials are stored securely in the Airflow UI. These are injected into dbt at runtime using Airflow task environment variables.
     - `FABRIC_TENANT_ID`
     - `FABRIC_TENANT_ID`
     - `FABRIC_CLIENT_ID`

## Pipeline Execution

The main pipeline is defined in `airflow/dags/dbt_fabric_pipeline.py` and includes:

1. **dbt deps**: Install dbt package dependencies
2. **Source Freshness**: Check data freshness for source tables
3. **dbt run**: Execute all dbt models
4. **dbt test**: Run data quality tests

### Manual Execution
- Trigger the `dbt_fabric_pipeline` DAG in Airflow UI

## Data Models

### Sources
- `fabric_bronze.customers`: Raw customer data
- `fabric_bronze.orders`: Raw order data

### Staging Models
- `stg_customer`: Cleaned customer data with proper types
- `stg_orders`: Cleaned order data

### Mart Models
- `dim_customers`: Customer dimension table
- `fact_orders`: Order facts table

## Configuration

### dbt Configuration
- **Profile**: `dbt_fabric`
- **Target**: `dev`
- **Materialization**: Tables for marts, views for staging

### Airflow Configuration
- **Schedule**: Daily execution
- **Executor**: LocalExecutor
- **Database**: PostgreSQL

## Monitoring and Logging

- **Airflow Logs**: Available in `airflow/logs/`
- **dbt Logs**: Available in `dbt_fabric/logs/`
- **Source Freshness**: Monitored with warning/error thresholds


## Troubleshooting

### Common Issues
1. **Fabric Connection**: Verify service principal credentials and permissions
2. **Docker Issues**: Ensure ports 8081, 5432 are available
3. **dbt Errors**: Check `dbt_fabric/target/run_results.json` for details

### Logs Location
- Airflow: `airflow/logs/`
- dbt: `dbt_fabric/logs/`


