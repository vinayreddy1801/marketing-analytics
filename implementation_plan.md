# Implementation Plan

## Phase 1: Setup
*   [ ] Git init and .gitignore creation.
*   [ ] Setup virtual environment (`venv`).
*   [ ] Install dependencies from requirements.txt.
*   [ ] Verify Python version.

## Phase 2: Data Engineering
*   [ ] Write `generate_spend_data.py` to create `marketing_spend.csv`.
    *   Logic: Correlate with TheLook event traffic.
*   [ ] Configure Google Cloud Platform Project.
*   [ ] Create BigQuery Dataset/Tables.
*   [ ] Configure Service Account and Secrets.

## Phase 3: SQL Core
*   [ ] Write Time-Decay Attribution Query.
*   [ ] Validate SQL against BigQuery public data.
*   [ ] Create View or Table for serving data.

## Phase 4: Frontend (Streamlit)
*   [ ] Initialize `app.py`.
*   [ ] Build Sidebar (Date Pickers, Filters).
*   [ ] Build KPI Row (ROAS, Spend, Revenue).
*   [ ] Build Attribution Comparator (Plotly Bar Chart).
*   [ ] Build Funnel Visualization.
*   [ ] Integrate NewsAPI for real-time context.

## Phase 5: Deployment
*   [ ] Push to GitHub.
*   [ ] Deploy to Streamlit Cloud.
*   [ ] Configure Secrets in Streamlit Cloud.
