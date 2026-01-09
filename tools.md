# Tool Selection & Justification

## Why Streamlit?
*   **Vs Tableau/PowerBI:** Code-first approach allows for version control (Git), deeper customization via Python, and demonstration of software engineering skills (API integration, secrets management).
*   **Vs React:** Rapid prototyping. We are data analysts, not frontend engineers. Streamlit provides "enough" UI for a data product without the overhead of a JS framework.

## Why Google BigQuery?
*   **Scale:** Serverless architecture handles petabytes. Use "TheLook" dataset (4M+ rows) effectively.
*   **Relevance:** Standard for modern "Modern Data Stack" companies.
*   **Features:** Strong support for Arrays/Structs (nested data) and standard SQL.

## Why Plotly?
*   **Interactivity:** Users can zoom, pan, and toggle series. Matplotlib is static.
*   **Integration:** Native support in Streamlit (`st.plotly_chart`).
