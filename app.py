from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('images')
        image_list = []

        for file in files:
            if file and file.filename:
                filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
                file.save(filepath)
                image = Image.open(filepath).convert('RGB')
                image_list.append(image)

        if image_list:
            pdf_path = os.path.join(UPLOAD_FOLDER, 'merged.pdf')
            image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
            return send_file(pdf_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
