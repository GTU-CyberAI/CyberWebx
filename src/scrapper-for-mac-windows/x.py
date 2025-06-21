from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

username = "jack"  # X (Twitter) kullanıcı adını buraya yaz
driver.get(f"https://twitter.com/{username}")
time.sleep(5)  # sayfanın yüklenmesini bekle

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

# Son tweet (ilk tweet'i çeker)
try:
    tweet = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text
except:
    tweet = "Yok"

print("👤 İsim:", name)
print("📝 Bio:", bio)
print("📍 Lokasyon:", location)
print("🔗 Website:", website)
print("📅 Katılım:", joined)
print("👥 Takipçi:", followers)
print("👥 Takip edilen:", following)
print("📢 Son Tweet:", tweet)

driver.quit()
