select
    CUSTOMER_ID,
    FIRST_NAME,
    LAST_NAME,
    COUNTRY,
    FIRST_NAME || ' ' || LAST_NAME as FULL_NAME,
    CREATED_AT
from {{ ref('silver_oracle_customers') }}