from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

# Configuration
KEY_PATH = 'creds.json'

def validate_query():
    print(f"Authenticating...")
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # Read Query
    with open('attribution_query.sql', 'r') as f:
        query = f.read()

    print("Running Attribution Query (this may take a moment)...")
    df = client.query(query).to_dataframe()
    
    print("\nQuery Result Preview:")
    print(df.head())
    
    print(f"\nTotal Rows: {len(df)}")
    
    if len(df) > 0:
        print("✅ SUCCESS: Query returned data.")
    else:
        print("⚠️ WARNING: Query returned no data.")

if __name__ == "__main__":
    validate_query()
