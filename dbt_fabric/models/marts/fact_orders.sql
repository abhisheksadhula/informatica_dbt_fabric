{{ config(materialized='table') }}

select
    ID

from {{ ref('stg_orders') }}
where STATUS = 'completed'
