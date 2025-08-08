from flask import Flask, request, send_file, render_template, redirect
import os
from encryption import encrypt_file, decrypt_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    encrypted_path = filepath + '.enc'
    encrypt_file(filepath, encrypted_path)
    os.remove(filepath)
    return redirect('/')

@app.route('/download/<filename>')
def download_file(filename):
    encrypted_path = os.path.join(UPLOAD_FOLDER, filename + '.enc')
    decrypted_path = os.path.join(UPLOAD_FOLDER, 'temp_' + filename)
    decrypt_file(encrypted_path, decrypted_path)
    return send_file(decrypted_path, as_attachment=True)

@app.after_request
def cleanup(response):
    for file in os.listdir(UPLOAD_FOLDER):
        if file.startswith("temp_"):
            os.remove(os.path.join(UPLOAD_FOLDER, file))
    return response

if __name__ == '__main__':
    app.run(debug=True)
