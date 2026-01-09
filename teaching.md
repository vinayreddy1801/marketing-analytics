# Teaching Concepts (Whiteboard Prep)

## 1. SQL Window Functions
*   **Concept:** Perform calculations across a set of table rows that are somehow related to the current row.
*   **Syntax:** `SUM(x) OVER (PARTITION BY y ORDER BY z)`
*   **Use Case:** In attribution, we use `SUM(raw_weight) OVER (PARTITION BY order_id)` to ensure the total attributed credit equals exactly 100% of the revenue, properly distributing it across multiple touchpoints.

## 2. Time Decay Attribution (Math)
*   **Concept:** Credits touchpoints based on recency. Closer to conversion = more credit.
*   **Formula:** $2^{-t/7}$ where $t$ is days relative to conversion.
    *   $t=0$ (Same day): $2^0 = 1$ (Full weight)
    *   $t=7$ (1 week ago): $2^{-1} = 0.5$ (Half weight)
*   **Why:** Acknowledges that recent interactions are more influential but doesn't ignore early awareness.

## 3. Python Generators & Distributions
*   **Concept:** Using statistical probability to generate fake but realistic data.
*   **Implementation:** `numpy.random.normal(loc=mean, scale=std_dev, size=n)`
*   **Why:** Real marketing data isn't flat. It has volatility. Using a normal distribution simulates daily CPC fluctuations naturally.
