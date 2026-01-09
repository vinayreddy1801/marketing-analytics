# Executive Marketing Command Center 🚀

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

A "Full Stack Analytics" portfolio project demonstrating end-to-end data engineering, advanced SQL logic, and interactive dashboard development. This project moves beyond static CSV analysis to simulate a modern enterprise data stack.

## 📊 Live Dashboard
**(Link to your deployed Streamlit Cloud app goes here after deployment)**

## 💼 Business Scenario
**Situation:** Marketing data was fragmented between advertising platforms (Spend) and the data warehouse (Revenue), leading to inaccurate budget allocation using default "Last-Click" attribution.
**Task:** Build a unified "Command Center" to reconcile Ad Spend vs. Revenue and implement a "Time-Decay" attribution model to better value upper-funnel interactions.
**Action:** Engineered a Python-Streamlit application connecting to Google BigQuery; generated synthetic cost data affecting 4M+ records; implemented complex Window Functions in SQL.
**Result:** Revealed that **Display Ads** were undervalued by 20% in the Last-Click model, enabling more efficient budget allocation.

## 🏗️ Architecture
*   **Data Warehouse:** Google BigQuery
    *   `bigquery-public-data.thelook_ecommerce` (Behavioral Data)
    *   `marketing_spend` (Synthetic Cost Data)
*   **ETL Pipeline:** Python script generating realistic cost data with seasonality & volatility.
*   **Frontend:** Streamlit (Python)
*   **Visualization:** Plotly Express

## 🚀 Key Features
1.  **Time-Decay Attribution:** Advanced SQL query transforming raw event logs into attributed revenue.
2.  **ROAS & CPA Calculators:** Real-time blending of Cost (Synthetic) and Revenue (Public Data).
3.  **Attribution Comparator:**  Side-by-side bar chart comparison of "Last Click" vs. "Time Decay" models.
4.  **Conversion Funnel:**  Visualizing the drop-off from `Product View` -> `Cart` -> `Purchase`.
5.  **Real-Time Context:** Integration with NewsAPI for live market headlines.

## 🛠️ Installation & Run Locally

1.  **Clone the Repo**
    ```bash
    git clone https://github.com/vinayreddy1801/marketing-analytics.git
    cd marketing-analytics
    ```

2.  **Install Dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure Credentials**
    *   Place your GCP Service Account JSON key in the root as `creds.json`.
    *   (Optional) Update `.streamlit/secrets.toml` for Cloud deployment.

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 📈 SQL Logic Preview
The core IP of this project is the Time-Decay Attribution query. It uses Window Functions to distribute credit:

```sql
normalized_attribution AS (
  SELECT
    *,
    raw_weight / SUM(raw_weight) OVER (PARTITION BY order_id) AS attributed_credit
  FROM weighted_paths
)
```

## 📄 License
This project is licensed under the terms of the GNU General Public License v3.0.