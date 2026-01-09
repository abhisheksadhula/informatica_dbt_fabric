{{ config(materialized='view') }}

select * from {{ source('fabric_bronze', 'orders') }}
