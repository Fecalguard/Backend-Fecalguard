from PIL import Image
import io
import numpy as np

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((244, 244))
    image_array = np.array(image) / 255.0
    return np.expand_dims(image_array, axis=0)