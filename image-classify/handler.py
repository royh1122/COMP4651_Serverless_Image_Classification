import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
import json

# Load MobileNet model
model = MobileNetV2(weights='imagenet')

def handle(req):
    """Handle an image classification request"""
    try:
        if not req:
            return json.dumps({"error": "Empty request body. Please provide an image for classification."})

        # Validate and decode the image
        try:
            img_tensor = tf.image.decode_image(req, channels=3)  # Decode as RGB
        except tf.errors.InvalidArgumentError:
            return json.dumps({"error": "Unsupported file format. Please provide a valid image file."})
        
        # Preprocess the image
        img_tensor = tf.image.resize(img_tensor, [224, 224])  # Resize to 224x224
        img_tensor = tf.expand_dims(img_tensor, axis=0)  # Add batch dimension
        img_tensor = preprocess_input(img_tensor)  # Apply preprocessing

        # Perform prediction
        predictions = model.predict(img_tensor)
        decoded = decode_predictions(predictions, top=3)

        # Format the output as JSON
        result = [{"label": label, "description": desc, "probability": float(prob)}
                  for (label, desc, prob) in decoded[0]]
        return json.dumps(result)

    except tf.errors.InvalidArgumentError:
        return json.dumps({"error": "Invalid input. Ensure the request contains a valid image."})

    except Exception as e:
        # Catch unexpected errors
        return json.dumps({"error": "An internal error occurred.", "details": str(e)})
