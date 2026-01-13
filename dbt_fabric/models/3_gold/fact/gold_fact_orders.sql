select *
from {{ ref('silver_orders') }}
where STATUS = 'completed'