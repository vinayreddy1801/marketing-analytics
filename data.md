# Data Dictionary & Logic

## TheLook Schema (BigQuery)
*   **`events`**: `id`, `user_id`, `sequence_number`, `session_id`, `created_at`, `ip_address`, `city`, `traffic_source`, `event_type`.
*   **`orders`**: `order_id`, `user_id`, `status`, `created_at`.
*   **`order_items`**: `id`, `order_id`, `user_id`, `product_id`, `sale_price`, `status`, `created_at`.
*   **`users`**: `id`, `first_name`, `last_name`, `email`, `traffic_source`, `created_at`.

## Synthetic Data Logic (`marketing_spend.csv`)
*   **Goal:** Simulate ad spend to allow ROAS calculation.
*   **Logic:**
    *   Base spend correlated with `traffic_source` volume in `events`.
    *   Channels: Search, Display, Facebook, Email.
    *   Noise introduced via normal distribution to simulate real-world volatility.
    *   Seasonality factor applied (e.g., Q4 spike).

## Data Quality Notes
*   **Revenue:** Assumes `order_items.status` NOT IN ('Cancelled', 'Returned') for finalized revenue.
*   **Attribution:** Time-decay model assumes a 7-day half-life.
