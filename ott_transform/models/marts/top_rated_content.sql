select
    title,
    platform,
    rating
from {{ ref('stg_raw_content') }}
where rating >= 7.5
order by rating desc
