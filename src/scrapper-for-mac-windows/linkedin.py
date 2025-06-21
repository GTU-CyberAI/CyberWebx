from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

# Kullanıcı bilgileri (SADECE KENDİ HESABIN İÇİN KULLAN)
username = "mens1studioo@gmail.com"
password = "Ahmet@123.!"
target = "ahmetyigit1"
# WebDriver başlat
options = Options()
options.add_argument('--disable-gpu')  # GPU kullanımını kapat
options.add_argument('--no-sandbox')   # Bazı sistemlerde sandbox hatalarını da önler
options.add_argument('--disable-dev-shm-usage')  # Low-memory sistemler için

driver = webdriver.Chrome(options=options)

# full ekranda aç
driver.maximize_window()

# LinkedIn'e git
driver.get("https://www.linkedin.com/login")

# Kullanıcı adı gir
email_field = driver.find_element(By.ID, "username")
email_field.send_keys(username)

# Şifre gir
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# Girişin ardından bekle
time.sleep(4)

# Profil sayfasına git
driver.get("https://www.linkedin.com/in/"+target+"/details/experience")  # kendi profilin

time.sleep(4)

# xpath ile profil bilgilerini çek
experience_items = driver.find_elements(By.CSS_SELECTOR, "li.pvs-list__paged-list-item")

for item in experience_items:
    try:
        title = item.find_element(By.CSS_SELECTOR, "div.t-bold span[aria-hidden='true']").text
    except:
        title = "Yok"

    try:
        company = item.find_element(By.XPATH, ".//a[contains(@href,'/company')]/span[aria-hidden='true']").text
    except:
        company = "Yok"

    try:
        duration = item.find_element(By.CSS_SELECTOR, "span.pvs-entity__caption-wrapper").text
    except:
        duration = "Yok"

    try:
        location_elem = item.find_elements(By.XPATH, ".//span[contains(text(), 'Türkiye') or contains(text(), 'Remote')]")
        location = location_elem[0].text if location_elem else "Yok"
    except:
        location = "Yok"

    try:
        # Açıklama: sadece ilk "t-black" class'lı açıklama kısmını alalım
        desc_elem = item.find_elements(By.CSS_SELECTOR, "div.t-black span[aria-hidden='true']")
        description = "\n".join([e.text for e in desc_elem if e.text.strip() != ""])
    except:
        description = "Yok"

    try:
        skills = item.find_element(By.XPATH, ".//strong[contains(text(),'Skills')]/..").text
    except:
        skills = "Yok"

    print("Pozisyon:", title)
    print("Şirket:", company)
    print("Süre:", duration)
    print("Lokasyon:", location)
    print("Açıklama:", description)
    print("Skills:", skills)
    print("------------\n")

# Tarayıcıyı kapat
driver.quit()
