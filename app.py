import os

# Optional: Comment this line out for testing if needed
# os.environ["TF_USE_LEGACY_KERAS"] = "1"

from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
import tensorflow as tf
import gdown

app = Flask(__name__)

MODEL_PATH = "wheat_model.keras"

# Download model if not present
if not os.path.exists(MODEL_PATH):
    gdown.download(
        "https://drive.google.com/uc?id=1-0XOfc83T0DRDYgDjQedPDlSXFhwaPIH",
        MODEL_PATH,
        quiet=False
    )

# Load model
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

print("=" * 60)
print("TF VERSION:", tf.__version__)
print("MODEL SHAPE:", model.input_shape)
print("MODEL FILE SIZE:", os.path.getsize(MODEL_PATH))
print("=" * 60)

classes = [
    'wheat_brown_rust',
    'wheat_healthy',
    'wheat_yellow_rust'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:

        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"})

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "Empty file"})

        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Invalid image"})

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = cv2.resize(img, (224, 224))
        img = img.astype("float32") / 255.0
        img = np.expand_dims(img, axis=0)

        print("Image Shape:", img.shape)
        print("Model Shape:", model.input_shape)

        pred = model.predict(img)

        print("Raw Prediction:", pred)

        class_index = np.argmax(pred)
        result = classes[class_index]
        confidence = float(np.max(pred)) * 100

        return jsonify({
            "prediction": result,
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
