/* 
   Time-Decay Attribution Model with Date Filter Support
*/

WITH user_paths AS (
  SELECT
    e.user_id,
    e.traffic_source,
    e.created_at AS touchpoint_time,
    o.order_id,
    o.created_at AS conversion_time,
    o.sale_price AS revenue,
    TIMESTAMP_DIFF(o.created_at, e.created_at, DAY) AS days_diff
  FROM `bigquery-public-data.thelook_ecommerce.events` e
  JOIN `bigquery-public-data.thelook_ecommerce.order_items` o
    ON e.user_id = o.user_id
  WHERE e.created_at < o.created_at
    AND e.created_at >= TIMESTAMP_SUB(o.created_at, INTERVAL 30 DAY) 
    AND e.traffic_source IN ('Facebook', 'Search', 'Display', 'Email', 'Organic') 
    AND o.status NOT IN ('Cancelled', 'Returned')
    -- DATE_FILTER_PLACEHOLDER
),

weighted_paths AS (
  SELECT
    *,
    POWER(2, - (days_diff / 7.0)) AS raw_weight
  FROM user_paths
),

normalized_attribution AS (
  SELECT
    *,
    raw_weight / SUM(raw_weight) OVER (PARTITION BY order_id) AS attributed_credit
  FROM weighted_paths
)

SELECT
  traffic_source,
  ROUND(SUM(attributed_credit * revenue), 2) AS time_decay_revenue,
  COUNT(DISTINCT order_id) as attributed_conversions
FROM normalized_attribution
GROUP BY 1
ORDER BY 2 DESC;
