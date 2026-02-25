import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import warnings

# Suppress TensorFlow warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Only show errors, not info/warnings

print("[INFO] Loading TensorFlow MobileNetV2 model...")
print(f"[INFO] TensorFlow version: {tf.__version__}")

model = None

try:
    # Load model once at startup
    print("[INFO] Downloading and loading MobileNetV2 model...")
    model = MobileNetV2(weights="imagenet")
    print("[INFO] ✓ MobileNetV2 model loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load MobileNetV2 model: {str(e)}")
    print("[INFO] Make sure TensorFlow is properly installed: pip install tensorflow")
    model = None

def predict_image(img_path):
    """Predict image class using pre-trained MobileNetV2 model"""
    try:
        if model is None:
            raise RuntimeError("Model not loaded. Check backend terminal for TensorFlow errors.")
            
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image file not found: {img_path}")
        
        # Verify file is readable
        if not os.access(img_path, os.R_OK):
            raise PermissionError(f"Cannot read image file (permission denied): {img_path}")
        
        file_size = os.path.getsize(img_path)
        print(f"[INFO] Image file size: {file_size} bytes")
        
        print(f"[INFO] Loading image from {img_path}")
        
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        print(f"[INFO] Image preprocessed successfully")

        print("[INFO] Making prediction...")
        predictions = model.predict(img_array, verbose=0)
        decoded = decode_predictions(predictions, top=1)
        
        if not decoded or not decoded[0]:
            raise ValueError("Model returned no predictions")

        result = decoded[0][0][1]
        confidence = float(decoded[0][0][2]) * 100
        print(f"[INFO] ✓ Prediction completed: {result} ({confidence:.1f}% confidence)")
        return f"{result} ({confidence:.1f}% confidence)"
    except Exception as e:
        error_msg = f"Error in predict_image: {str(e)}"
        print(f"[ERROR] {error_msg}")
        raise