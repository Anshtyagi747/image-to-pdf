from flask import Flask, request, send_file
from PIL import Image
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("images")

    file_paths = []

    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        file_paths.append(path)

    # 🔥 SORT (img_123 type support)
    def extract_number(path):
        name = os.path.basename(path)
        nums = re.findall(r'\d+', name)
        return int(nums[0]) if nums else 0

    file_paths.sort(key=extract_number)

    images = []
    for path in file_paths:
        img = Image.open(path).convert("RGB")
        images.append(img)

    pdf_path = "output.pdf"

    if images:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])

    # delete temp images
    for path in file_paths:
        os.remove(path)

    # 🔥 IMPORTANT for mobile download
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="my_images.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
