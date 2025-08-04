#  Secure File Sharing System – Cybersecurity Internship Project

This project was developed as part of **Cyber Security Task 3** in the **Future Interns Internship Program**. It simulates a secure file sharing environment, integrating AES encryption to protect files during upload, storage, and download.

---

##  Project Overview

The system is a simple web-based file sharing platform built with **Python Flask**. It encrypts uploaded files using **AES (Advanced Encryption Standard)** and stores them in an unreadable format. Files are decrypted automatically upon download, ensuring confidentiality and integrity throughout the process.

---

##  Key Features

-  File encryption using AES (EAX mode)  
-  Encrypted file storage with `.enc` extension  
-  User-friendly web interface for file upload/download  
-  On-demand decryption during file retrieval  
-  Temporary decrypted files are automatically removed post-download  

---

##  Project Objectives

- Apply cryptographic techniques to secure file handling  
- Gain hands-on experience with Flask and web development  
- Understand encryption key management and data protection best practices  
- Demonstrate real-world implementation of secure data workflows  

---

##  Scope of Work

| Area | Details |
|------|---------|
|  Backend Logic | Flask server with secure upload/download routes |
|  Encryption Engine | AES encryption implemented using PyCryptodome |
|  Frontend | HTML-based UI for interacting with the system |
|  Integration | Connects frontend, backend, and encryption workflows |
|  Testing | Manual testing of encryption, decryption, and integrity |

---

##  Set-up Instructions

### Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Virtualenv (recommended)

---

##  PHASE 1: Setup Your Kali Linux Environment

### Step 1. Open Terminal and Update
```
sudo apt update && sudo apt upgrade -y
```

### Step 2. Install Python3, pip, and virtualenv (if not already)
```
sudo apt install python3 python3-pip python3-venv -y
```

### Step 3. Create Your Project Folder
```
mkdir secure-file-share && cd secure-file-share
python3 -m venv venv
source venv/bin/activate
```

### Step 4. Install Flask and PyCryptodome
```
pip install Flask pycryptodome
```

---

## PHASE 2: Basic Flask App Structure

### Step 5. Create Files
```
touch app.py encryption.py
mkdir templates static uploads
```

### Project Structure Preview
```
secure-file-share/
│
├── app.py                 # Flask main server
├── encryption.py          # AES functions
├── templates/
│   └── index.html         # Upload/download UI
├── static/                # CSS/JS if needed
└── uploads/               # Encrypted files
```

---

## PHASE 3: Build Encryption with AES

### Step 6. Add AES encryption logic in `encryption.py`
Paste this in:
```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

key = b'ThisIsASecretKey'  # In production, use secure key mgmt!

def encrypt_file(input_file, output_file):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(input_file, 'rb') as f:
        data = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(output_file, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

def decrypt_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    with open(output_file, 'wb') as f:
        f.write(data)
```

---

##  PHASE 4: Flask Routes for Upload and Download

###  Step 7. Paste this into `app.py`

```python
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
```

---

##  PHASE 5: Create Basic HTML Template

### Step 8. `templates/index.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Secure File Sharing</title>
</head>
<body>
    <h1>Upload a File</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file" required />
        <button type="submit">Upload</button>
    </form>

    <h2>Encrypted Files</h2>
    <ul>
        {% for file in files %}
        <li>
            {{ file }}
            <a href="/download/{{ file }}">Download</a>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
```

---

## PHASE 6: Run the Web App
```
python app.py
```

Then visit:

```
http://127.0.0.1:5000
```

Upload a file → It gets encrypted → You can download it (auto-decrypted for user).

---

## PHASE 7: Test & Take Screenshots

* Upload a `.txt` or `.jpg` file
* Check `/uploads/` for `.enc` file
* Use Postman or `curl` to test endpoints if you like
* Take screenshots of:

  * Upload screen
  * Upload action in terminal
  * Encrypted file in `/uploads`
  * Successful file download

---


```
