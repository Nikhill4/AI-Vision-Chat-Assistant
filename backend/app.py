from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
import tempfile
from image_model import predict_image
from chatbot import get_bot_response

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Accept"],
    "supports_credentials": True
}})

print("[INFO] CORS enabled for all origins and methods")

# Use system temp folder instead of OneDrive folder (avoid sync issues)
# This is MUCH more reliable than OneDrive storage
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "ai_vision_uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"[INFO] Created uploads folder at {UPLOAD_FOLDER}")
else:
    print(f"[INFO] Uploads folder exists at {UPLOAD_FOLDER}")

print("[INFO] Flask app initializing...")
print(f"[INFO] Upload folder: {UPLOAD_FOLDER}")
print("[INFO] ⚠️  Using system temp folder to avoid OneDrive sync issues")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "message": "AI Vision Chat Assistant Backend Running!"})

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    try:
        if "image" not in request.files:
            print("[ERROR] No image file in request")
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]
        if file.filename == '':
            print("[ERROR] Empty filename")
            return jsonify({"error": "No file selected"}), 400

        # Validate file extension
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            print(f"[ERROR] Invalid file type: {file.filename}")
            return jsonify({"error": "Invalid file type. Only image files allowed."}), 400

        print(f"[INFO] Processing image: {file.filename}")
        
        # Ensure UPLOAD_FOLDER exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            print(f"[INFO] Created uploads folder: {UPLOAD_FOLDER}")
        
        # Use safe filename without spaces (UUID + extension)
        import uuid
        file_ext = os.path.splitext(file.filename)[1].lower()
        safe_filename = f"image_{uuid.uuid4().hex}{file_ext}"
        filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
        print(f"[INFO] Original filename: {file.filename}")
        print(f"[INFO] Safe filename: {safe_filename}")
        print(f"[INFO] Saving to: {filepath}")
        
        # Save file
        file.save(filepath)
        print(f"[INFO] File saved successfully")
        
        # Verify file was saved
        if not os.path.exists(filepath):
            raise RuntimeError(f"File save failed - file not found at {filepath}")
        
        file_size = os.path.getsize(filepath)
        print(f"[INFO] File size: {file_size} bytes")
        
        if file_size == 0:
            raise ValueError("Saved file is empty")
        
        # Wait a moment for OneDrive sync
        import time
        time.sleep(0.5)
        
        # Double-check file still exists (OneDrive may have moved it)
        if not os.path.exists(filepath):
            raise RuntimeError(f"File lost after save - OneDrive may have moved it: {filepath}")

        prediction = predict_image(filepath)
        print(f"[INFO] Prediction result: {prediction}")

        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        error_msg = f"Error in predict: {str(e)}"
        print(f"[ERROR] {error_msg}")
        traceback.print_exc()
        return jsonify({"error": error_msg}), 500

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({}), 200
        
    try:
        data = request.get_json()
        if not data:
            print("[ERROR] No JSON data in request")
            return jsonify({"error": "No data provided"}), 400

        user_message = data.get("message", "")
        if not user_message.strip():
            print("[ERROR] Empty message")
            return jsonify({"error": "Message cannot be empty"}), 400

        print(f"[INFO] User message: {user_message}")
        reply = get_bot_response(user_message)
        print(f"[INFO] Bot reply: {reply}")

        return jsonify({"reply": reply}), 200
    except Exception as e:
        error_msg = f"Error in chat: {str(e)}"
        print(f"[ERROR] {error_msg}")
        traceback.print_exc()
        return jsonify({"error": error_msg}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("[INFO] Starting Flask application...")
    print("[INFO] Backend server will run on http://localhost:5000")
    print("[INFO] CORS enabled for all origins")
    print("[INFO] Listening on 0.0.0.0:5000 (all interfaces)")
    try:
        # Use 0.0.0.0 to listen on all interfaces, disable debug to avoid reloader issues
        app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)
    except Exception as e:
        print(f"[ERROR] Failed to start Flask: {str(e)}")
        traceback.print_exc()
        sys.exit(1)