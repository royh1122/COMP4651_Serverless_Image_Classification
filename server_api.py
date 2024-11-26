from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load MobileNetV2 model
model = MobileNetV2(weights='imagenet')

@app.route("/predict", methods=["POST"])
def classify_image():
    """Handle an image classification request"""
    try:
        # Check if the request contains data
        if not request.data:
            return jsonify({"error": "Empty request body. Please provide an image for classification."}), 400

        # Validate and decode the image
        try:
            img_tensor = tf.image.decode_image(request.data, channels=3)  # Decode as RGB
        except tf.errors.InvalidArgumentError:
            return jsonify({"error": "Unsupported file format. Please provide a valid image file."}), 400

        # Preprocess the image
        img_tensor = tf.image.resize(img_tensor, [224, 224])  # Resize to 224x224
        img_tensor = tf.expand_dims(img_tensor, axis=0)  # Add batch dimension
        img_tensor = preprocess_input(img_tensor)  # Apply MobileNetV2 preprocessing

        # Perform prediction
        predictions = model.predict(img_tensor)
        decoded = decode_predictions(predictions, top=3)

        # Format the output as JSON
        result = [{"label": label, "description": desc, "probability": float(prob)}
                  for (label, desc, prob) in decoded[0]]
        return jsonify(result)

    except Exception as e:
        # Catch unexpected errors
        return jsonify({"error": "An internal error occurred.", "details": str(e)}), 500

# Run the Flask app locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
