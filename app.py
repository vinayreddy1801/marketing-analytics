import streamlit as st
import plotly.express as px
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import requests

# Page Config
st.set_page_config(
    page_title="Executive Marketing Command Center",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" Look
st.markdown("""
<style>
    .metric-card {
        background-color: #0E1117;
        border: 1px solid #262730;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
    }
    .metric-title {
        color: #979797;
        font-size: 14px;
        font-weight: 500;
    }
    .metric-value {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
    }
    .metric-delta {
        font-size: 12px;
        font-weight: 500;
    }
    .positive { color: #00CC96; }
    .negative { color: #EF553B; }
</style>
""", unsafe_allow_html=True)

# -----------------
# DATA LOADING
# -----------------
# -----------------
# DATA LOADING
# -----------------
@st.cache_data(ttl=3600)
def load_data(start_date=None, end_date=None):
    # Authentication
    # Use st.secrets if available (Cloud), else local JSON
    if "gcp_service_account" in st.secrets:
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
    else:
        # Fallback for local development if secrets.toml isn't used
        creds = service_account.Credentials.from_service_account_file("creds.json")
    
    client = bigquery.Client(credentials=creds, project=creds.project_id)

    # Date Filter Clause
    date_filter = ""
    if start_date and end_date:
        date_filter = f"AND date BETWEEN '{start_date}' AND '{end_date}'"
        # For TheLook data which uses created_at timestamp
        timestamp_filter = f"AND created_at BETWEEN '{start_date}' AND '{end_date}'"
        # For order_items and events
        o_timestamp_filter = f"AND o.created_at BETWEEN '{start_date}' AND '{end_date}'"
        e_timestamp_filter = f"AND e.created_at BETWEEN '{start_date}' AND '{end_date}'"
    else:
        timestamp_filter = ""
        o_timestamp_filter = ""
        e_timestamp_filter = ""


    # 1. Fetch Attribution Query (Revenue)
    # Inject Date Filter into the SQL
    with open('attribution_query.sql', 'r') as f:
        base_sql = f.read()
    
    # Inject Date Filter
    if start_date and end_date:
        sql = base_sql.replace("-- DATE_FILTER_PLACEHOLDER", f"AND o.created_at BETWEEN '{start_date}' AND '{end_date}'")
    else:
        sql = base_sql.replace("-- DATE_FILTER_PLACEHOLDER", "")
    
    df_revenue = client.query(sql).to_dataframe()

    # 2. Fetch Marketing Spend (Cost)
    sql_cost = f"""
        SELECT 
            utm_source as traffic_source, 
            SUM(cost) as total_cost,
            SUM(clicks) as total_clicks,
            SUM(impressions) as total_impressions 
        FROM `marketing-ops-portfolio.portfolio_staging.marketing_spend`
        WHERE 1=1 {date_filter}
        GROUP BY 1
    """
    df_cost = client.query(sql_cost).to_dataframe()
    
    # 3. Fetch Last Click Revenue
    sql_last_click = f"""
        SELECT 
            traffic_source,
            SUM(sale_price) as last_click_revenue
        FROM `bigquery-public-data.thelook_ecommerce.order_items` o
        JOIN `bigquery-public-data.thelook_ecommerce.users` u ON o.user_id = u.id
        WHERE o.status NOT IN ('Cancelled', 'Returned')
        {o_timestamp_filter}
        GROUP BY 1
    """
    df_last_click = client.query(sql_last_click).to_dataframe()

    # 4. Fetch Funnel Data
    sql_funnel = f"""
        SELECT 
            traffic_source,
            event_type,
            COUNT(DISTINCT session_id) as sessions
        FROM `bigquery-public-data.thelook_ecommerce.events` e
        WHERE event_type IN ('product', 'cart', 'purchase')
        {e_timestamp_filter}
        GROUP BY 1, 2
    """
    df_funnel = client.query(sql_funnel).to_dataframe()

    return df_revenue, df_cost, df_last_click, df_funnel

# -----------------
# SIDEBAR
# -----------------
from datetime import date, timedelta

# ... (Previous imports)

# -----------------
# SIDEBAR
# -----------------
with st.sidebar:
    st.title("Admin Controls")
    st.markdown("---")
    
    # Date Picker with Defaults to prevent UI Glitches
    today = date.today()
    default_start = today - timedelta(days=30)
    min_date = date(2019, 1, 1) # Start of TheLook data
    
    date_range = st.date_input(
        "Analysis Window", 
        value=(default_start, today),
        min_value=min_date,
        max_value=today
    )
    
    start_date = None
    end_date = None
    if len(date_range) == 2:
        start_date = date_range[0]
        end_date = date_range[1]
    
    # Debug Secrets (Remove in Production)
    # with st.expander("Debug Secrets"):
    #     st.write(st.secrets.keys())
        
    st.markdown("### Real-Time Market News")
    # NewsAPI Integration
    try:
        # Check both top-level and nested to be safe
        # st.secrets behaves like a dictionary.
        # If news_api_key is at the top level it should be accessible.
        
        api_key = None
        if "news_api_key" in st.secrets:
            api_key = st.secrets["news_api_key"]
        elif "gcp_service_account" in st.secrets and "news_api_key" in st.secrets["gcp_service_account"]:
             # Fallback if user nested it inside [gcp_service_account] by accident
             api_key = st.secrets["gcp_service_account"].get("news_api_key")
        
        if api_key:
            # Broader query to ensure results
            url = f"https://newsapi.org/v2/everything?q=marketing&sortBy=publishedAt&apiKey={api_key}&language=en&pageSize=3"
            news = requests.get(url).json()
            
            if news.get('articles'):
                for article in news['articles']:
                    st.markdown(f"**[{article['title']}]({article['url']})**")
                    st.caption(f"Source: {article['source']['name']}")
                    st.markdown("---")
            else:
                st.info("No news found")
        else:
             st.warning("News API Key missing in secrets")
            
    except Exception:
        st.warning("News feed unavailable")

# Load Data with Date Filter
try:
    df_revenue, df_cost, df_last_click, df_funnel = load_data(start_date, end_date)
    
    # Filter Attribution Data (df_revenue) via Pandas since we didn't inject SQL
    # Note: df_revenue needs a date column to filter! The current query sums it up.
    # We need to modify the attribution query to return daily data if we want to filter it here, 
    # OR we ignore date filter for attribution structure for now (awkward).
    # Let's modify attribution_query.sql to Return Order Date so we can filter.

    
    # Merge Data for Master Table
    # Left join because Organic has revenue but no cost
    df_master = df_revenue.merge(df_cost, on='traffic_source', how='left')
    df_master = df_master.merge(df_last_click, on='traffic_source', how='left')
    
    # Handle NaNs (Organic cost = 0)
    df_master.fillna(0, inplace=True)
    
    # Calculate ROAS and CPA
    df_master['ROAS'] = df_master.apply(lambda x: x['time_decay_revenue'] / x['total_cost'] if x['total_cost'] > 0 else 0, axis=1)
    df_master['CPA'] = df_master.apply(lambda x: x['total_cost'] / x['attributed_conversions'] if x['attributed_conversions'] > 0 else 0, axis=1)
    
except Exception as e:
    st.error(f"Data Connection Error: {e}")
    st.stop()



# -----------------
# MAIN DASHBOARD
# -----------------

st.title("Executive Marketing Command Center v1.1 (Debug)")
st.markdown("Real-time performance monitoring across all acquisition channels.")

# KPI Row
col1, col2, col3, col4 = st.columns(4)

total_revenue = df_master['time_decay_revenue'].sum()
total_spend = df_master['total_cost'].sum()
global_roas = total_revenue / total_spend if total_spend > 0 else 0
total_conversions = df_master['attributed_conversions'].sum()

col1.metric("Total Revenue (Time Decay)", f"${total_revenue:,.0f}")
col2.metric("Total Ad Spend", f"${total_spend:,.0f}")
col3.metric("Global ROAS", f"{global_roas:.2f}x")
col4.metric("Total Conversions", f"{total_conversions:,.0f}")

st.markdown("---")

# Visualizations

c1, c2 = st.columns((2,1))

with c1:
    st.subheader("Attribution Model Comparison")
    st.caption("Does our default 'Last Click' model undervalue upper-funnel channels?")
    
    # Prepare Data for Plotly Grouped Bar
    df_melt = df_master[['traffic_source', 'time_decay_revenue', 'last_click_revenue']].melt(
        id_vars='traffic_source', 
        var_name='Model', 
        value_name='Revenue'
    )
    
    fig_bar = px.bar(
        df_melt, 
        x='traffic_source', 
        y='Revenue', 
        color='Model', 
        barmode='group',
        color_discrete_sequence=['#00CC96', '#636EFA'],
        template="plotly_dark"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("Channel Efficiency (ROAS)")
    fig_scatter = px.scatter(
        df_master[df_master['total_cost'] > 0],
        x='total_cost',
        y='time_decay_revenue',
        size='attributed_conversions',
        color='traffic_source',
        template="plotly_dark",
        labels={'total_cost': 'Spend', 'time_decay_revenue': 'Revenue'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

st.markdown("---")

# Debugging Info
st.info(f"📅 Active Date Range: {start_date} to {end_date}")

# Debugging: RAW CHECK (Unfiltered)
# We run a tiny separate query to prove connection to Test Data, ignoring date filters
# Use explicit credentials from secrets
creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])
client = bigquery.Client(credentials=creds, project=creds.project_id)

st.info(f"Connected to Project: `{client.project}`")

debug_sql = "SELECT * FROM `marketing-ops-portfolio.portfolio_staging.marketing_spend` WHERE utm_source = 'Test_Channel'"
try:
    df_debug = client.query(debug_sql).to_dataframe()
    if not df_debug.empty:
        st.warning("⚠️ PROOF MODE: Test Data Exists in BigQuery (ignoring filters)")
        st.dataframe(df_debug)
    else:
        st.error(f"Test Data NOT found. table: `marketing_spend` row_count: {df_debug.shape[0]}")
except Exception as e:
    st.error(f"Debug Query Failed: {e}")

# Funnel Visualization
st.subheader("Conversion Funnel Analysis")
st.caption("Session drop-off from Product View to Purchase (Last 90 Days)")

# Process Funnel Data
# Order of stages
funnel_stages = ['product', 'cart', 'purchase']
df_funnel['event_type'] = pd.Categorical(df_funnel['event_type'], categories=funnel_stages, ordered=True)
df_funnel = df_funnel.sort_values('event_type')

# Filter for top sources to avoid clutter
top_sources = ['Search', 'Organic', 'Facebook', 'Email', 'Display']
df_funnel_filtered = df_funnel[df_funnel['traffic_source'].isin(top_sources)]

fig_funnel = px.funnel(
    df_funnel_filtered, 
    x='sessions', 
    y='event_type', 
    color='traffic_source',
    template="plotly_dark"
)
st.plotly_chart(fig_funnel, use_container_width=True)

# Data Table
st.subheader("Detailed Performance")
st.dataframe(
    df_master[['traffic_source', 'total_cost', 'time_decay_revenue', 'ROAS', 'CPA', 'attributed_conversions']]
    .style.format({
        'total_cost': '${:,.2f}', 
        'time_decay_revenue': '${:,.2f}',
        'ROAS': '{:.2f}x',
        'CPA': '${:,.2f}',
        'attributed_conversions': '{:,.0f}'
    })
)
