import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json

gcp_cred_str = os.getenv("GCP_KEY")
if not gcp_cred_str:
    raise ValueError("GCP_KEY environment variable is not set")

# Parse the GCP credentials from the environment variable
gcp_cred = json.loads(gcp_cred_str)

# Initialize Firebase Admin SDK with GCP credentials
cred = credentials.Certificate(gcp_cred)

# Initialize Firebase Admin SDK
firebase_admin.initialize_app(cred)
db = firestore.client()