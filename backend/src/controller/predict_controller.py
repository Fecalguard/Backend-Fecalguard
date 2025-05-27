from fastapi import UploadFile, HTTPException
import tensorflow as tf
import numpy as np
from src.util.preprocess_image import preprocess_image 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from google.cloud import storage
from google.oauth2 import service_account
import uuid

# Use the application default credentials.
cred = credentials.Certificate('./gcp-key.json')

# Initialize Firebase Admin SDK
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Google Cloud Storage
gcp_credentials = service_account.Credentials.from_service_account_file('./gcp-key.json')
storage_client = storage.Client(credentials=gcp_credentials)
bucket_name = 'fecal-guard'

# Load model
model = tf.keras.models.load_model("./model/model.h5")

# Daftar label
# CLASS_NAMES = ['AFRICAN LEOPARD', 'CARACAL', 'CHEETAH', 'CLOUDED LEOPARD', 'JAGUAR', 'LIONS', 'OCELOT', 'PUMA', 'SNOW LEOPARD', 'TIGER']
CLASS_NAMES = ['Coccidiosis', 'Healthy', 'New Castle Disease', 'Salmonella']

async def predict(file: UploadFile):
    try:
        image_bytes = await file.read()
        processed_image = preprocess_image(image_bytes)

        prediction = model.predict(processed_image)
        predicted_index = int(np.argmax(prediction, axis=1)[0])
        confidence = float(np.max(prediction))

        identifier = str(uuid.uuid4())

        # Save image to Google Cloud Storage
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f'prediction-images/{identifier}.jpg')
        blob.upload_from_string(image_bytes, content_type='image/jpeg')
        
        result = {
            "predicted_class": CLASS_NAMES[predicted_index],
            "confidence": confidence,
            "image_url": blob.public_url,
            "datetime": datetime.now().isoformat(),
        }

        # Save prediction to Firestore
        doc_ref = db.collection('predictions').document(identifier)
        doc_ref.set(result)

        return result
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_prediction_history():
    history_ref = db.collection('predictions')
    docs = history_ref.stream()
    
    history = []
    for doc in docs:
        history.append(doc.to_dict())

    return history