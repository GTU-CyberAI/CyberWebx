import apiurl
import sys
sys.modules['__main__'] = apiurl
from flask import Flask, request, jsonify
import joblib
import os
import time
import pyfiglet
import joblib

# same as app.py but not ui
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

app = Flask(__name__)

# Load the model once at startup
model = joblib.load("Classifier/url_model.pkl")

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
        result = 'good'
    else:
        try:
            result = model.predict([url])[0]
        except Exception as e:
            return jsonify({'error': 'Model prediction failed', 'details': str(e)}), 500

    return jsonify({'url': url, 'result': result})


@app.route('/')
def home():
    return "Malware Detector API is running. Use POST /check-url with JSON {'url': 'example.com'}"

if __name__ == '__main__':
    app.run(debug=True)
