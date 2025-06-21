from flask import Flask, request, jsonify
import platform
import os
import uuid
from model import MalwareModel
from scanWindows import scan_pe_file as scan_pe_file_windows
from scanLinux import scan_pe_file as scan_pe_file_linux

app = Flask(__name__)
UPLOAD_DIR = "./test"
os.makedirs(UPLOAD_DIR, exist_ok=True)

system = platform.system().lower()
model = MalwareModel(
    model_path='Classifier/finalized_model.sav',
    scaler_path='Classifier/scaler.pkl'
)

@app.route('/scan-file', methods=['POST'])
def scan_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'Filename is empty'}), 400

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{uploaded_file.filename}")
    uploaded_file.save(file_path)

    try:
        if system == 'windows':
            result = scan_pe_file_windows(file_path, model)
        elif system == 'linux':
            result = scan_pe_file_linux(file_path, model)
        else:
            return jsonify({'error': f'Unsupported OS: {system}'}), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': 'Scan failed', 'details': str(e)}), 500

    finally:
        try:
            os.remove(file_path)
        except Exception:
            pass
        for temp in ["scanList.csv", "PEfiles.txt"]:
            if os.path.exists(temp):
                os.remove(temp)

@app.route('/generate-password', methods=['POST'])
def generate_password():
    data = request.get_json()
    if not data or 'scraper_output' not in data:
        return jsonify({'error': 'Missing scraper_output'}), 400

    scraper_output = data['scraper_output']

    passwords = []
    for i in range(10):
        suffix = random.randint(100, 999)  # 3 basamaklı rastgele sayı
        new_password = f"gen-{scraper_output[::-1]}-{suffix}"
        passwords.append(new_password)

    return jsonify({'passwords': passwords})


@app.route('/')
def home():
    return "Malware Detector API is running. Use POST /scan-file to upload and scan a PE file."

if __name__ == '__main__':
    app.run(debug=True)
