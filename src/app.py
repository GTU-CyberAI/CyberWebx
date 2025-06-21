import sys
import app
sys.modules['__main__'] = app

from flask import Flask, request, jsonify, render_template
import joblib
import os
import time
import pyfiglet
import platform
import uuid
from model import MalwareModel
from scanWindows import scan_pe_file as scan_pe_file_windows
from scanLinux import scan_pe_file as scan_pe_file_linux
import requests

app = Flask(__name__)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = "AIzaSyAUY3fsceC1KKoJbdWINFSf9K5TcdqaoY8"
# === URL Scanner Setup ===
def sanitization(web):
    web = web.lower()
    token = []
    dot_token_slash = []
    raw_slash = str(web).split('/')
    for i in raw_slash:
        raw1 = str(i).split('-')
        slash_token = []
        for j in range(len(raw1)):
            raw2 = str(raw1[j]).split('.')
            slash_token += raw2
        dot_token_slash += raw1 + slash_token
    token = list(set(dot_token_slash))
    if 'com' in token:
        token.remove('com')
    return token

# Load the URL model once at startup
url_model = joblib.load("Classifier/url_model.pkl")
# Whitelist of known good domains
WHITELIST = {'hackthebox.eu', 'root-me.org', 'gmail.com'}

@app.route('/check-url', methods=['POST'])
def check_url():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" in request body'}), 400

    url = data['url'].strip().lower()

    # Bypass whitelist
    if url in WHITELIST:
        return jsonify({'url': url, 'result': 'good'})

    try:
        result = url_model.predict([url])[0]
    except Exception as e:
        return jsonify({'error': 'Model prediction failed', 'details': str(e)}), 500

    response_data = {'url': url, 'result': result}
    if result == 'bad':
        prompt = (
            f"This URL has been detected as malicious: {url}. "
            f"Please explain in 3 clear sentences why this kind of domain is considered dangerous, "
            f"based on general cybersecurity principles (such as phishing, malware, typosquatting, spam). "
            f"Do not include any extra commentary, just the explanation."
        )

        try:
            gemini_response = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [
                        {
                            "parts": [
                                {"text": prompt}
                            ]
                        }
                    ]
                }
            )
            gemini_response.raise_for_status()
            gemini_data = gemini_response.json()
            explanation = gemini_data['candidates'][0]['content']['parts'][0]['text']
            response_data['urlDetailResult'] = explanation
            print(explanation)

        except Exception as e:
            return jsonify({'error': 'Gemini API failed', 'details': str(e)}), 500

    return jsonify(response_data)


# === File Scanner Setup ===
UPLOAD_DIR = "./test"
os.makedirs(UPLOAD_DIR, exist_ok=True)

system = platform.system().lower()
malware_model = MalwareModel(
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
            result = scan_pe_file_windows(file_path, malware_model)
        elif system in ['linux', 'darwin']:
            result = scan_pe_file_linux(file_path, malware_model)
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

    prompt = (
     "You are a password generation expert. Based on the following scraped data from LinkedIn, Twitter, and Instagram, generate *500 unique and strong passwords* that are also memorable for the user.\n"

     "- Include some traditional patterns.\n"

     "- Incorporate personal but public details to make the passwords strong yet easy to remember.\n"

     "- Avoid weak or common passwords unless they are personalized.\n"

    "- Vary the format, use substitutions (like @ for a), camelCase, numbers, and symbols where suitable.\n"
    "- Use at least one upper-lower case - numbers - special characters in %10.\n"
    "- Also you can add some specific of user's name-surname personel information.\n"

    "- Do *not* include any explanations, comments, or headers.\n"

     "- Return only the passwords, one per line.\n\n"
    f"Scraped Input:\n{scraper_output}"
    )

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
        )
        response.raise_for_status()
        gemini_data = response.json()

        raw_text = gemini_data['candidates'][0]['content']['parts'][0]['text']
        passwords = [line.strip() for line in raw_text.split('\n') if line.strip()]

        return jsonify({'passwords': passwords})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Gemini API request failed', 'details': str(e)}), 500

    except (KeyError, IndexError) as e:
        return jsonify({'error': 'Invalid response from Gemini API', 'details': str(e)}), 500
# === Default route ===
@app.route('/')
def home():
    return render_template('index.html')  

# === Run server ===
if __name__ == '__main__':
    app.run(debug=True)
