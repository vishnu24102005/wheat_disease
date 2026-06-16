import os
from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import gdown

app = Flask(__name__)

# Model file
MODEL_PATH = "wheat_model.h5"

# Download model if not present
if not os.path.exists(MODEL_PATH):
    gdown.download(
        "https://drive.google.com/uc?id=1PXbqamHEvHkgtkrUhBfUrQRunHZ8Evdg",
        MODEL_PATH,
        quiet=False
    )

# Load model
model = load_model(MODEL_PATH, compile=False)

print("=" * 60)
print("MODEL LOADED SUCCESSFULLY")
print("TF VERSION:", tf.__version__)
print("MODEL SHAPE:", model.input_shape)
print("MODEL FILE SIZE:", os.path.getsize(MODEL_PATH))
print("=" * 60)

# Class labels
classes = [
    "wheat_brown_rust",
    "wheat_healthy",
    "wheat_yellow_rust"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        # Read image
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image"}), 400

        # Preprocess image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img.astype("float32") / 255.0
        img = np.expand_dims(img, axis=0)

        print("Image Shape:", img.shape)
        print("Model Shape:", model.input_shape)

        # Predict
        prediction = model.predict(img, verbose=0)

        print("Raw Prediction:", prediction)

        class_index = int(np.argmax(prediction))
        confidence = float(np.max(prediction)) * 100

        return jsonify({
            "prediction": classes[class_index],
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
