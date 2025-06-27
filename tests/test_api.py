import os
import requests

BASE_URL = "http://127.0.0.1:5000"
OUTPUT_FILE = "run-result.txt"


def write_result(title, success, detail=""):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        status = "OK" if success else "FAIL"
        f.write(f"{title}: {status}\n")
        if detail:
            f.write(f"   Detail: {detail}\n")


def test_home():
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        write_result("test_home", True)
    except Exception as e:
        write_result("test_home", False, str(e))


def test_scan_file_valid():
    try:
        file_path = "sample_pe_file.exe"
        if not os.path.exists(file_path):
            write_result("test_scan_file_valid", False, "sample_pe_file.exe bulunamadı.")
            return
        with open(file_path, "rb") as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/scan-file", files=files)
        assert response.status_code in [200, 500]
        data = response.json()
        assert "prediction" in data or "error" in data
        write_result("test_scan_file_valid", True)
    except Exception as e:
        write_result("test_scan_file_valid", False, str(e))


def test_scan_file_empty():
    try:
        files = {'file': ("", b"")}
        response = requests.post(f"{BASE_URL}/scan-file", files=files)
        assert response.status_code == 400
        assert response.json().get("error") == "Filename is empty"
        write_result("test_scan_file_empty", True)
    except Exception as e:
        write_result("test_scan_file_empty", False, str(e))


def test_check_url_valid():
    try:
        payload = {"url": "http://example.com"}
        response = requests.post(f"{BASE_URL}/check-url", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        write_result("test_check_url_valid", True)
    except Exception as e:
        write_result("test_check_url_valid", False, str(e))


def test_check_url_missing():
    try:
        response = requests.post(f"{BASE_URL}/check-url", json={})
        assert response.status_code == 400
        assert response.json().get("error") == 'Missing "url" in request body'
        write_result("test_check_url_missing", True)
    except Exception as e:
        write_result("test_check_url_missing", False, str(e))


def test_generate_password_valid():
    try:
        payload = {
            "scraper_output": "ahmetyigit twitter linkedin gmail123 instagrambio hacker123"
        }
        response = requests.post(f"{BASE_URL}/generate-password", json=payload)
        assert response.status_code in [200, 500]  # 500 olabilir çünkü Gemini API key expired olabilir
        data = response.json()
        if "passwords" in data:
            assert isinstance(data["passwords"], list)
            write_result("test_generate_password_valid", True)
        else:
            write_result("test_generate_password_valid", False, str(data))
    except Exception as e:
        write_result("test_generate_password_valid", False, str(e))


def test_generate_password_missing():
    try:
        response = requests.post(f"{BASE_URL}/generate-password", json={})
        assert response.status_code == 400
        assert response.json().get("error") == "Missing scraper_output"
        write_result("test_generate_password_missing", True)
    except Exception as e:
        write_result("test_generate_password_missing", False, str(e))


if __name__ == "__main__":
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    test_home()
    test_scan_file_valid()
    test_scan_file_empty()
    test_check_url_valid()
    test_check_url_missing()
    test_generate_password_valid()
    test_generate_password_missing()

    print("Tüm testler tamamlandı. Sonuçlar run-result.txt içinde.")
