from flask import Flask, request, jsonify
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from io import BytesIO

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

model_name = "realfake2"
model = load_model(f"{model_name}/keras_model.h5", compile=False)
class_names = open(f"{model_name}/labels.txt", "r").readlines()
np.set_printoptions(suppress=True)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data, verbose=0)
    index = np.argmax(prediction)

    # class_name = class_names[index]
    confidence_score = prediction[0][index]
    pred_verb = str(class_names[index][2:]).strip().lower()
    return [prediction, confidence_score, pred_verb]


@app.route('/')
def hello():
    return "Send me an image and I'll predict if it's PCC or real life :D"


@app.route('/help')
def helproute():
    return ("Make a POST request to '/check' and make sure that you add a form-data body with 'file' as key and your "
            "image as your value")


@app.route('/check', methods=['POST'])
def check():
    print(request.data)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file is allowed
    if file and allowed_file(file.filename):
        # Secure the filename and save the file

        result = predict(file.stream.read())
        print(result)

        # Return a success message with the file path
        return jsonify({
            'message': 'File analysed successfully',
            'output': {
                'prediction': f'{result[2]}',
                'confidence': float(result[1])
            }
        }), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3032)
