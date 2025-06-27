# 📌 Project Title: CyberWebX - An Intelligent Cybersecurity Platform

## 📖 Project Description

CyberWebX is a modular and intelligent cybersecurity platform designed to tackle modern digital threats through a combination of machine learning and Open-Source Intelligence (OSINT). The project's primary goal is to provide a unified, user-friendly interface for several critical security functions: static analysis of executable files for malware detection, lexical and feature-based analysis of URLs for phishing detection, and the generation of highly secure passwords based on OSINT-derived data.

The system is architected around a central Flask REST API, which serves both a web-based dashboard and exposes endpoints for programmatic use. This modular design allows for easy extension and integration of new security tools in the future. A key component is the standalone OSINT scraper, built with Tkinter, which runs locally on the user's machine to ensure that potentially sensitive data is never exposed to the cloud. This project is intended for educational and research purposes to demonstrate the practical application of data science in cybersecurity.

---

## 🌟 Key Features

* **Machine Learning-Powered Detection:** Utilizes Random Forest and Logistic Regression models for high-accuracy malware and phishing analysis.
* **OSINT-Enhanced Password Security:** Leverages a local data scraper and the Gemini LLM API to generate strong, context-aware passwords that are difficult to guess.
* **Modular REST API:** Built with Flask, providing separate, well-defined endpoints for each core function, making the system extensible and easy to maintain.
* **Interactive Web Dashboard:** A simple frontend built with HTML, CSS, and JavaScript that allows users to interact with the file scanner and URL checker.
* **Privacy-Focused Data Scraping:** Includes a standalone Tkinter GUI application for local OSINT gathering, ensuring user data privacy.

---

## 📁 Repository Structure & File Explanations

This project is organized into a logical directory structure to separate concerns and improve maintainability. Below is an explanation of each key file and directory.

| File / Directory | Purpose & Key Components |
| :--- | :--- |
| **`/src`** | The main directory containing all the application's source code. |
| ↳ `app.py` | **Main Application File:** This is the entry point for the Flask backend. It initializes the Flask app, defines all API routes (`@app.route`), handles incoming HTTP requests, and sends back JSON responses. Key functions route traffic for URL checking, file scanning, and password generation. |
| ↳ `model.py` | **ML Model Handler:** This module is responsible for loading the pre-trained machine learning models (e.g., from `.pkl` files) into memory. It provides simple functions that the Flask app can call to get predictions without needing to know the underlying model implementation. |
| ↳ `/ML_Model`, `/Classifier`| **Machine Learning Artifacts:** These directories store the serialized, pre-trained machine learning models (e.g., `url_classifier.pkl`, `malware_detector.pkl`). Separating them keeps the main source code clean. |
| ↳ `/scraper-for-mac-windows` | **Local OSINT Scraper:** Contains the source code for the standalone GUI application built with Tkinter. It runs independently of the web server to scrape data from local sources or the web, which is then used for password generation. `guimain.py` is likely the entry point. |
| ↳ `/static` | **Frontend Assets:** Standard Flask directory for all static files that are served directly to the client's browser, such as CSS stylesheets, JavaScript files, and images. |
| ↳ `/templates` | **HTML Views:** Standard Flask directory containing all Jinja2 HTML templates. These files are rendered by Flask to create the web pages a user sees, such as the main dashboard, upload forms, and results pages. |
| **`/tests`** | **Testing API's:** It holds the PNG screenshots used in this README for demonstration purposes. |
| **`/tests`** | **Testing Directory:** Contains automated integration tests (`test_runner.py`) that send requests to the live Flask server and verify key endpoints such as `/`, `/scan-file`, `/check-url`, and `/generate-password`. Results are saved to `run-result.txt`.|
| `requirements.txt` | **Project Dependencies:** This critical file lists all the Python packages required to run the project (e.g., `flask`, `scikit-learn`, `pandas`). It allows anyone to create an identical environment using `pip install -r requirements.txt`. |
| `Procfile` | **Deployment Configuration:** A file used by cloud hosting platforms like Heroku to understand how to run the application. It typically contains a command like `web: gunicorn app:app`. |
| `.gitignore` | **Version Control Exclusions:** Specifies files and directories that Git should ignore, such as `__pycache__`, virtual environment folders (`venv/`), and sensitive credential files. |
| `README.md` | **Project Documentation:** This file. It provides a comprehensive overview and instructions for the project. |

*Note: Clean, informative comments are included within the source code files (`.py`) to explain the functionality of important functions and classes, their inputs/outputs, and any limitations.*

---

## 🛠️ Installation Instructions

Follow these steps to set up and run the project on your local machine.

1.  **Clone the Repository**
    Open your terminal, navigate to the directory where you want to store the project, and run the following command:
    ```bash
    git clone [https://github.com/Mens1s/CyberWebX.git](https://github.com/Mens1s/CyberWebX.git)
    cd CyberWebX
    ```

2.  **Create and Activate a Virtual Environment**
    It is highly recommended to use a virtual environment to isolate project dependencies and avoid conflicts.
    * **On macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Required Dependencies**
    The `requirements.txt` file contains all necessary packages. Install them with a single command:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Flask Application**
    Start the backend server by running the main application file:
    ```bash
    python src/app.py
    ```
    The server will start, and you can access the web dashboard at `http://127.0.0.1:5000` in your browser.

---

## ▶️ Usage Examples

The platform can be used via the web dashboard or by making direct API calls.

#### 1. Checking a URL for Phishing
Send a `POST` request to the `/check-url` endpoint with the URL in the JSON body.

* **Sample Request (`curl`):**
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"url": "[http://google-update-account-info.com](http://google-update-account-info.com)"}' \
    [http://127.0.0.1:5000/check-url](http://127.0.0.1:5000/check-url)
    ```
* **Sample Response (Malicious):**
    ```json
    {
      "result": "bad",
      "url": "[http://google-update-account-info.com](http://google-update-account-info.com)"
    }
    ```

#### 2. Scanning a File for Malware
Use the web dashboard to upload an executable file. The backend will process it and return a result indicating if the file is `legitimate` or `malicious`.

#### 3. Generating a Secure Password
Send a `POST` request to `/generate-password` with OSINT data.

* **Sample Request (`curl`):**
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{"user_data": "John Doe born 1990 loves dogs named Buddy"}' \
    [http://127.0.0.1:5000/generate-password](http://127.0.0.1:5000/generate-password)
    ```
* **Sample Response:**
    ```json
    {
      "passwords": [
        "Jd-Buddy!1990",
        "D0gL0ver#90",
        "..."
      ]
    }
    ```

---

## 🧩 Troubleshooting

If you encounter issues, refer to the common problems and solutions below.

* **Error: `ModuleNotFoundError: No module named 'flask'`**
    * **Cause:** The required dependencies are not installed, or you are not in the correct virtual environment.
    * **Solution:** Ensure your virtual environment is activated and run `pip install -r requirements.txt`.

* **Error: `FileNotFoundError: [Errno 2] No such file or directory: 'ML_Model/model.pkl'`**
    * **Cause:** The application cannot find the pre-trained model files.
    * **Solution:** Verify that the model files exist in the correct directories (`src/ML_Model/` or `src/Classifier/`) and that the file paths in `src/model.py` are correct relative to the application's root.

* **Error: `500 Internal Server Error` when using Password Generator**
    * **Cause:** The Gemini API key is either missing or invalid.
    * **Solution:** Ensure your API key is correctly set up as an environment variable or in a configuration file that is read by `app.py`. Do not hardcode secrets in the source code.

* **Error: `OSError: [WinError 10013] Address already in use`**
    * **Cause:** Another application is already using port 5000.
    * **Solution:** Stop the other application or run the Flask app on a different port by modifying `app.py`: `app.run(port=5001)`.

---

### 🎯 Goals & Use Cases
- Demonstrate ML usage in malware and phishing detection
- Provide local OSINT-based password generation
- Show Flask API modularity with frontend + backend integration

---

## 🤝 Acknowledgements

This project was developed as part of the coursework for the **CSE 473 - Network And Information Security** course, under the instruction of **Dr. Öğr. Üyesi Salih Sarp**.

* **Lead Developers & Collaborators:**
    * Ahmet Yiğit (a.yigit2020@gtu.edu.tr)
    * Emre Oytun
    * Elif Deniz