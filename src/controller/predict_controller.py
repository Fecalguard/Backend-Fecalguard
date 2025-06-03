from fastapi import UploadFile, HTTPException
import tensorflow as tf
import numpy as np
from src.util.preprocess_image import preprocess_image 
from datetime import datetime
import uuid
from src.service.object_storage import storage_client, bucket_name
from src.service.database import db
import requests

url = "https://storage.googleapis.com/fecal-guard/model/vgg16_model.h5"
local_path = "vgg16_model.h5"

# Unduh model dari cloud storage
response = requests.get(url)
with open(local_path, 'wb') as f:
    f.write(response.content)

# Load model dari file lokal
model = tf.keras.models.load_model(local_path)

# Daftar label
CLASS_NAMES = ['Coccidiosis', 'Healthy', 'New Castle Disease', 'Salmonella']

async def predict(file: UploadFile, current_user: dict):
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
            "current_user": current_user.get("username"),
        }

        # Save prediction to Firestore
        doc_ref = db.collection('predictions').document(identifier)
        doc_ref.set(result)

        return result
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_prediction_history(current_user: dict):
    user_predictions_ref = db.collection('predictions').where('current_user', '==', current_user.get("username"))
    user_predictions = user_predictions_ref.stream()
    history = []
    for doc in user_predictions:
        history.append(doc.to_dict())

    return history