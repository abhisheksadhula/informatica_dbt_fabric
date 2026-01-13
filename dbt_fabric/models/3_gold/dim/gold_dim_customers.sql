select
    ID,
    FIRST_NAME,
    LAST_NAME,
    concat(FIRST_NAME, ' ', LAST_NAME) as FULL_NAME
from {{ ref('silver_customers') }}