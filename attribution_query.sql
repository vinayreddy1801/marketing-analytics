/* 
   Time-Decay Attribution Model
   Logic: 
   1. Identify all marketing touchpoints (events) prior to a conversion (order).
   2. Apply a decay formula: 2^(-days_diff/7). 7 days is the half-life.
   3. Normalize weights so they sum to 100% per order.
   4. Aggregate revenue by channel.
*/

WITH user_paths AS (
  -- CTE 1: Identify all marketing interactions prior to conversion
  -- We join events to order_items to find successful conversions
  SELECT
    e.user_id,
    e.traffic_source,
    e.created_at AS touchpoint_time,
    o.order_id,
    o.created_at AS conversion_time,
    o.sale_price AS revenue,
    -- Calculate days between touchpoint and conversion for decay logic
    TIMESTAMP_DIFF(o.created_at, e.created_at, DAY) AS days_diff
  FROM `bigquery-public-data.thelook_ecommerce.events` e
  JOIN `bigquery-public-data.thelook_ecommerce.order_items` o
    ON e.user_id = o.user_id
  WHERE e.created_at < o.created_at
    -- Attribution Window: Only look back 30 days
    AND e.created_at >= TIMESTAMP_SUB(o.created_at, INTERVAL 30 DAY) 
    -- Filter out internal traffic or non-marketing events if necessary
    AND e.traffic_source IN ('Facebook', 'Search', 'Display', 'Email', 'Organic') 
    AND o.status NOT IN ('Cancelled', 'Returned')
),

weighted_paths AS (
  -- CTE 2: Apply the Time Decay Formula
  -- Formula: 2^(-days/7). 7 days is the half-life.
  SELECT
    *,
    POWER(2, - (days_diff / 7.0)) AS raw_weight
  FROM user_paths
),

normalized_attribution AS (
  -- CTE 3: Normalize weights so they sum to 1 per order
  SELECT
    *,
    raw_weight / SUM(raw_weight) OVER (PARTITION BY order_id) AS attributed_credit
  FROM weighted_paths
)

-- Final Output: Aggregated Revenue per Channel based on Time Decay
SELECT
  traffic_source,
  ROUND(SUM(attributed_credit * revenue), 2) AS time_decay_revenue,
  COUNT(DISTINCT order_id) as attributed_conversions
FROM normalized_attribution
GROUP BY 1
ORDER BY 2 DESC;
