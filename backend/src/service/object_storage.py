from google.cloud import storage
from google.oauth2 import service_account

# Initialize Google Cloud Storage
gcp_credentials = service_account.Credentials.from_service_account_file('./gcp-key.json')
storage_client = storage.Client(credentials=gcp_credentials)
bucket_name = 'fecal-guard'