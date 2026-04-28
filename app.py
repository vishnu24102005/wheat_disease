from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load model
model = load_model("wheat_model.h5")


classes = ['wheat_brown_rust', 'wheat_healthy', 'wheat_yellow_rust']


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


        img = cv2.resize(img, (224, 224)) / 255.0
        img = np.reshape(img, (1, 224, 224, 3))

  
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
        return jsonify({"error": str(e)})

# this is the development code 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)