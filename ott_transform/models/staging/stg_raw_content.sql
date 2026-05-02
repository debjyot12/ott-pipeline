select
    title,
    platform,
    rating,
    loaded_at,
    current_timestamp as dbt_updated_at
from {{ source('public', 'raw_content') }}
where title is not null
  and rating is not null
