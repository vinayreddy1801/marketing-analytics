from google.cloud import bigquery
from google.oauth2 import service_account

KEY_PATH = "creds.json"

def cleanup_data():
    print("Authenticating...")
    creds = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = bigquery.Client(credentials=creds, project=creds.project_id)
    
    print("Deleting Test_Channel data...")
    sql = "DELETE FROM `marketing-ops-portfolio.portfolio_staging.marketing_spend` WHERE utm_source = 'Test_Channel'"
    client.query(sql).result() # Wait for job to finish
    print("✅ Cleanup Complete. Test data removed.")

if __name__ == "__main__":
    cleanup_data()
