from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_unique_pdf_name(base_folder, base_name="anshpdf", ext=".pdf"):
    i = 1
    while os.path.exists(os.path.join(base_folder, f"{base_name}{i}{ext}")):
        i += 1
    return os.path.join(base_folder, f"{base_name}{i}{ext}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('images')
        image_list = []

        for file in files:
            if file and file.filename:
                filepath = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
                file.save(filepath)
                try:
                    image = Image.open(filepath).convert('RGB')
                    image_list.append(image)
                except Exception as e:
                    print(f"Error processing image {file.filename}: {e}")

        if image_list:
            pdf_path = get_unique_pdf_name(UPLOAD_FOLDER)
            image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:], resolution=100.0)
            return send_file(pdf_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
