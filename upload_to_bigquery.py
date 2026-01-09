from google.cloud import bigquery
from google.oauth2 import service_account
import os

# Configuration
KEY_PATH = 'creds.json'
PROJECT_ID = 'marketing-ops-portfolio'
DATASET_ID = 'portfolio_staging'
TABLE_ID = 'marketing_spend'
CSV_FILE = 'marketing_spend_simulated.csv'

def upload_to_bigquery():
    print(f"Authenticating with {KEY_PATH}...")
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 1. Create Dataset if it doesn't exist
    dataset_ref = client.dataset(DATASET_ID)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {DATASET_ID} already exists.")
    except Exception:
        print(f"Creating dataset {DATASET_ID}...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Dataset {DATASET_ID} created.")

    # 2. Configure Load Job
    table_ref = dataset_ref.table(TABLE_ID)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1, 
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE # Overwrite if exists
    )

    # 3. Upload File
    print(f"Uploading {CSV_FILE} to {DATASET_ID}.{TABLE_ID}...")
    with open(CSV_FILE, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Waits for the job to complete.
    
    table = client.get_table(table_ref)
    print(f"Loaded {table.num_rows} rows to {TABLE_ID}.")

if __name__ == "__main__":
    if not os.path.exists(KEY_PATH):
        print(f"Error: {KEY_PATH} not found. Please place the JSON key file in the root directory.")
    elif not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found. Please run generate_spend_data.py first.")
    else:
        try:
            upload_to_bigquery()
        except Exception as e:
            with open("error.log", "w") as f:
                f.write(f"TYPE: {type(e).__name__}\n")
                f.write(f"MSG: {str(e)}\n")
            print("Error logged to error.log")
