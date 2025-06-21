from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import instaloader

output_lines = []  # Notepad için içerik tutucu

# LinkedIn bilgileri
linkedin_username = "mens1studioo@gmail.com"
linkedin_password = "Ahmet@123.!"
linkedin_target = "ahmetyigit1"

# Twitter bilgileri
twitter_username = "jack"

# Instagram bilgileri
instagram_username = "instagram"  # çekmek istediğin kullanıcı adı

# WebDriver başlat
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# ---------------- LINKEDIN ----------------
driver.get("https://www.linkedin.com/login")

email_field = driver.find_element(By.ID, "username")
email_field.send_keys(linkedin_username)

password_field = driver.find_element(By.ID, "password")
password_field.send_keys(linkedin_password)
password_field.send_keys(Keys.RETURN)

time.sleep(4)

driver.get("https://www.linkedin.com/in/" + linkedin_target + "/details/experience")
time.sleep(4)

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
        desc_elem = item.find_elements(By.CSS_SELECTOR, "div.t-black span[aria-hidden='true']")
        description = "\n".join([e.text for e in desc_elem if e.text.strip() != ""])
    except:
        description = "Yok"

    try:
        skills = item.find_element(By.XPATH, ".//strong[contains(text(),'Skills')]/..").text
    except:
        skills = "Yok"

    section = [
        f"LinkedIn Pozisyon: {title}",
        f"LinkedIn Şirket: {company}",
        f"LinkedIn Süre: {duration}",
        f"LinkedIn Lokasyon: {location}",
        f"LinkedIn Açıklama: {description}",
        f"LinkedIn Skills: {skills}",
        "------------\n"
    ]

    for line in section:
        print(line)
        output_lines.append(line)

# ---------------- TWITTER ----------------
driver.get(f"https://twitter.com/{twitter_username}")
time.sleep(5)

try:
    name = driver.find_element(By.XPATH, '//div[@data-testid="UserName"]//span').text
except:
    name = "Yok"

try:
    bio = driver.find_element(By.XPATH, '//div[@data-testid="UserDescription"]').text
except:
    bio = "Yok"

try:
    joined = driver.find_element(By.XPATH, '//span[contains(text(), "Joined")]').text
except:
    joined = "Yok"

try:
    followers = driver.find_element(By.XPATH, '//a[contains(@href,"/followers")]//span[1]').text
    following = driver.find_element(By.XPATH, '//a[contains(@href,"/following")]//span[1]').text
except:
    followers = following = "Yok"

try:
    location = driver.find_element(By.XPATH, '//span[contains(@data-testid,"UserLocation")]').text
except:
    location = "Yok"

try:
    website = driver.find_element(By.XPATH, '//span[contains(@data-testid,"UserUrl")]').text
except:
    website = "Yok"

try:
    tweet = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text
except:
    tweet = "Yok"

twitter_section = [
    f"Twitter İsim: {name}",
    f"Twitter Bio: {bio}",
    f"Twitter Lokasyon: {location}",
    f"Twitter Website: {website}",
    f"Twitter Katılım: {joined}",
    f"Twitter Takipçi: {followers}",
    f"Twitter Takip Edilen: {following}",
    f"Twitter Son Tweet: {tweet}"
]

for line in twitter_section:
    print(line)
    output_lines.append(line)

# Tarayıcıyı kapat
driver.quit()

# ---------------- INSTAGRAM ----------------
L = instaloader.Instaloader()

try:
    profile = instaloader.Profile.from_username(L.context, instagram_username)

    instagram_section = [
        f"Instagram Kullanıcı Adı: {profile.username}",
        f"Instagram Ad: {profile.full_name}",
        f"Instagram Bio: {profile.biography}",
        f"Instagram Website: {profile.external_url}",
        f"Instagram Takipçi: {profile.followers}",
        f"Instagram Takip Edilen: {profile.followees}",
        f"Instagram Gönderi Sayısı: {profile.mediacount}"
    ]

    for line in instagram_section:
        print(line)
        output_lines.append(line)

except Exception as e:
    error_line = f"Instagram profil bilgileri çekilemedi: {e}"
    print(error_line)
    output_lines.append(error_line)

# ---------------- NOTEPAD (TXT) KAYDET ----------------
with open("social_media_report.txt", "w", encoding="utf-8") as f:
    for line in output_lines:
        f.write(line + "\n")

print("\n✅ Tüm bilgiler 'social_media_report.txt' dosyasına kaydedildi.")
