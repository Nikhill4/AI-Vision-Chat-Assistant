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


def _prepare_image_variants(img_path):
    """Create multiple views of the same image for more stable predictions."""
    base_img = image.load_img(img_path, target_size=(256, 256))
    base_array = image.img_to_array(base_img)

    center = base_array[16:240, 16:240, :]
    h_flip = np.fliplr(center)
    original_224 = base_array[16:240, 16:240, :]

    variants = np.stack([original_224, center, h_flip], axis=0)
    return preprocess_input(variants.copy())


def _decode_top_predictions(probabilities, top=3):
    decoded = decode_predictions(np.expand_dims(probabilities, axis=0), top=top)
    return [
        {
            "class_id": item[0],
            "label": item[1].replace("_", " "),
            "confidence": round(float(item[2]) * 100, 2)
        }
        for item in decoded[0]
    ]

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

        img_batch = _prepare_image_variants(img_path)
        print(f"[INFO] Image preprocessed successfully")

        print("[INFO] Making prediction...")
        predictions = model.predict(img_batch, verbose=0)
        averaged_prediction = np.mean(predictions, axis=0)

        top_predictions = _decode_top_predictions(averaged_prediction, top=3)

        if not top_predictions:
            raise ValueError("Model returned no predictions")

        primary = top_predictions[0]
        summary = f"Likely {primary['label']} ({primary['confidence']:.1f}% confidence)"
        print(f"[INFO] ✓ Prediction completed: {summary}")

        return {
            "prediction": summary,
            "primary_label": primary["label"],
            "primary_confidence": primary["confidence"],
            "top_predictions": top_predictions,
            "summary": summary
        }
    except Exception as e:
        error_msg = f"Error in predict_image: {str(e)}"
        print(f"[ERROR] {error_msg}")
        raise