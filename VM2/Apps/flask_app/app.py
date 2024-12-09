from flask import Flask, request, jsonify
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import base64
from PIL import Image
import io

app = Flask(__name__)

# Load ResNet50 model
model = ResNet50(weights='imagenet')

def preprocess_image(img):
    """Preprocess image for ResNet50."""
    img = img.resize((224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

@app.route('/', methods=['POST'])
def infer():
    """Perform inference on received image."""
    data = request.get_json()
    img_data = base64.b64decode(data['image'])
    img = Image.open(io.BytesIO(img_data))
    processed_img = preprocess_image(img)
    preds = model.predict(processed_img)
    decoded_preds = decode_predictions(preds, top=1)[0][0]
    return jsonify({"inferred": decoded_preds[1]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)