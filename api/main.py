from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def blur_background(image_path, blur_strength=15):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read image.")

    blur_strength = max(1, int(blur_strength // 2) * 2 + 1)
    blurred_image = cv2.GaussianBlur(image, (blur_strength, blur_strength), 0)
    return blurred_image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No file uploaded', 400

        file = request.files['image']
        if file.filename == '':
            return 'No selected file', 400

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            blur_strength = int(request.form.get('blur_strength', 15))

            blurred_image = blur_background(file_path, blur_strength)

            blurred_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"blurred_{filename}")
            cv2.imwrite(blurred_image_path, blurred_image)

            return render_template('index.html', original_image=file_path, blurred_image=blurred_image_path, blur_strength=blur_strength)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
