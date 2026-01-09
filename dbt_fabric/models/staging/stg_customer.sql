{{ config(materialized='view') }}

select
    cast(ID as int) as customer_id,
    trim(cast(FIRST_NAME as varchar(100))) as first_name,
    trim(cast(LAST_NAME as varchar(100)))  as last_name

from {{ source('fabric_bronze', 'customers') }}
