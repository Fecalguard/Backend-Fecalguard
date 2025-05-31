from google.cloud import storage
from google.oauth2 import service_account
import os
import json

# Load GCP credentials from environment variable or file
gcp_cred_str = os.getenv("GCP_KEY")
if not gcp_cred_str:
    raise ValueError("GCP_KEY environment variable is not set")

# Parse the GCP credentials from the environment variable
gcp_cred = json.loads(gcp_cred_str)

# Create a credentials object
gcp_credentials = service_account.Credentials.from_service_account_info(gcp_cred)
storage_client = storage.Client(credentials=gcp_credentials)
bucket_name = 'fecal-guard'