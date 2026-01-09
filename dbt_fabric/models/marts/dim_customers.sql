{{ config(materialized='table') }}

select
    customer_id,
    first_name,
    last_name,
    concat(first_name, ' ', last_name) as full_name

from {{ ref('stg_customer') }}
