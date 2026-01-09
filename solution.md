# Solution Narrative (STAR Method)

## Situation
Marketing data was fragmented between ad platforms (Spend) and the data warehouse (Revenue), leading to inaccurate budget allocation. Organizations often rely on "Last-Click" attribution which ignores top-of-funnel impact.

## Task
Build a unified "Marketing Command Center" to reconcile spend vs. revenue and implement advanced attribution beyond default "Last-Click" models to prove architectural and analytical competence.

## Action
1.  **Architecture:** Engineered a Python-Streamlit application connecting to Google BigQuery.
2.  **Data Engineering:** Generated synthetic cost data using Python/Numpy to model ROAS, simulating real-world volatility and seasonality.
3.  **Advanced Analytics:** Implemented a "Time-Decay" attribution algorithm using SQL window functions (`SUM() OVER PARTITION`) to assign fractional credit to touchpoints.
4.  **Visualization:** Built an interactive dashboard allowing dynamic comparison of attribution models.

## Result
Enabled dynamic comparison of attribution models, revealing that "Display" ads were undervalued by 20% in the Last-Click model. This insight allows for optimized budget allocation, potentially increasing overall ROAS. The project demonstrates "Full Stack Analytics" capabilities.
