# Key Performance Indicators (KPIs)

## 1. ROAS (Return on Ad Spend)
*   **Formula:** `Attributed Revenue / Marketing Spend`
*   **SQL Logic:** `SUM(attributed_revenue) / SUM(cost)`
*   **Business Value:** Measures the efficiency of advertising dollars. Target > 4.0.

## 2. CPA (Cost Per Acquisition)
*   **Formula:** `Marketing Spend / Total Orders`
*   **SQL Logic:** `SUM(cost) / COUNT(DISTINCT order_id)`
*   **Business Value:** Measures the cost to acquire a paying customer. Lower is better.

## 3. Conversion Rate
*   **Formula:** `Unique Sessions with Purchase / Total Unique Sessions`
*   **Business Value:** Measures site effectiveness.

## 4. AOV (Average Order Value)
*   **Formula:** `Total Revenue / Total Orders`
*   **SQL Logic:** `SUM(sale_price) / COUNT(DISTINCT order_id)`
*   **Business Value:** revenue per transaction.

## 5. CLV (Customer Lifetime Value)
*   **Formula:** `Average Purchase Value * Purchase Frequency * Customer Lifespan`
*   **Proxied via:** 12-Month Revenue per User.
