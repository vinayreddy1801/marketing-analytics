from google.cloud import bigquery
from google.oauth2 import service_account
import os

# Path to your JSON key
KEY_PATH = "creds.json"

def check_data():
    print("Authenticating...")
    creds = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = bigquery.Client(credentials=creds, project=creds.project_id)
    
    print("Checking for Test_Channel in marketing_spend...")
    sql = """
        SELECT * 
        FROM `marketing-ops-portfolio.portfolio_staging.marketing_spend` 
        WHERE utm_source = 'Test_Channel'
    """
    df = client.query(sql).to_dataframe()
    
    if not df.empty:
        print("✅ SUCCESS: Found Test_Channel data!")
        print(df)
    else:
        print("❌ FAILURE: No data found for Test_Channel.")
        print("This means the INSERT didn't work, OR the project/dataset names are mismatched.")

if __name__ == "__main__":
    check_data()
