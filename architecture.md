# Architecture

## Data Sources
*   **Primary:** `bigquery-public-data.thelook_ecommerce` (BigQuery) - Read-only behavioral data.
*   **Secondary:** `marketing_spend.csv` (Synthetic) - Simulated ad spend (Facebook, Search, Email, Display).
*   **Tertiary:** NewsAPI (Real-time) - Live industry context.

## Data Pipeline
1.  **Extract:** SQL pulls from BigQuery; Python generates cost data.
2.  **Transform:** Python merges cost/revenue; SQL Window functions calculate Attribution.
3.  **Load:** Aggregated data served to Streamlit.

## Tech Stack
*   **Language:** Python 3.10+
*   **Frontend:** Streamlit
*   **Visualization:** Plotly
*   **Compute:** Google Cloud BigQuery
*   **Manipulation:** Pandas

## Entity Relationship Diagram (ERD)
*   `events.user_id` -> `users.id`
*   `order_items.order_id` -> `orders.order_id`
*   `order_items.user_id` -> `users.id`
*   `inventory_items.product_id` -> `order_items.product_id`
