from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image, ImageFilter
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def blur_background(image_path, blur_strength=15):
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(blur_strength))
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
            blurred_image.save(blurred_image_path)

            return render_template('index.html', original_image=file_path, blurred_image=blurred_image_path, blur_strength=blur_strength)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
