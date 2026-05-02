select
    platform,
    count(*) as total_titles,
    round(avg(rating), 2) as avg_rating,
    max(rating) as highest_rating,
    min(rating) as lowest_rating
from {{ ref('stg_raw_content') }}
group by platform
order by avg_rating desc
