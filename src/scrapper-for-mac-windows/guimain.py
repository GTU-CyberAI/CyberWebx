import tkinter as tk
from tkinter import messagebox
import instaloader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

def run_script():
    linkedin_username = "mens1studioo@gmail.com"
    linkedin_password = "Ahmet@123.!"
    linkedin_target = entry_linkedin_target.get().strip()
    twitter_username = entry_twitter_user.get().strip()
    instagram_username = entry_instagram_user.get().strip()

    output_lines = []

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = None
    try:
        if linkedin_target or twitter_username:
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()

        # LinkedIn
        if linkedin_target:
            driver.get("https://www.linkedin.com/login")
            driver.find_element(By.ID, "username").send_keys(linkedin_username)
            driver.find_element(By.ID, "password").send_keys(linkedin_password)
            driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
            time.sleep(4)
            driver.get(f"https://www.linkedin.com/in/{linkedin_target}")
            time.sleep(4)

            # İl / ilçe bilgisi
            try:
                location_info = driver.find_element(By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]').text
            except:
                location_info = "Yok"

            # Şu an nerede çalışıyor
            try:
                current_position = driver.find_element(By.XPATH, '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]').text
            except:
                current_position = "Yok"

            profile_section = [
                f"LinkedIn İl / İlçe: {location_info}",
                f"LinkedIn Şu Anki Pozisyon: {current_position}",
                "------------\n"
            ]
            output_lines.extend(profile_section)
            driver.get(f"https://www.linkedin.com/in/{linkedin_target}/details/experience")
            time.sleep(4)

            experience_items = driver.find_elements(By.CSS_SELECTOR, "li.pvs-list__paged-list-item")
            for item in experience_items:
                username = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").text if driver.find_elements(By.CSS_SELECTOR, "h1.text-heading-xlarge") else "Yok"
                title = item.find_element(By.CSS_SELECTOR, "div.t-bold span[aria-hidden='true']").text if item.find_elements(By.CSS_SELECTOR, "div.t-bold span[aria-hidden='true']") else "Yok"
                company = item.find_element(By.XPATH, ".//a[contains(@href,'/company')]/span[aria-hidden='true']").text if item.find_elements(By.XPATH, ".//a[contains(@href,'/company')]/span[aria-hidden='true']") else "Yok"
                duration = item.find_element(By.CSS_SELECTOR, "span.pvs-entity__caption-wrapper").text if item.find_elements(By.CSS_SELECTOR, "span.pvs-entity__caption-wrapper") else "Yok"
                location_elem = item.find_elements(By.XPATH, ".//span[contains(text(), 'Türkiye') or contains(text(), 'Remote')]")
                location = location_elem[0].text if location_elem else "Yok"
                desc_elem = item.find_elements(By.CSS_SELECTOR, "div.t-black span[aria-hidden='true']")
                description = "\n".join([e.text for e in desc_elem if e.text.strip() != ""]) if desc_elem else "Yok"
                skills = item.find_element(By.XPATH, ".//strong[contains(text(),'Skills')]/..").text if item.find_elements(By.XPATH, ".//strong[contains(text(),'Skills')]/..") else "Yok"

                section = [
                    f"LinkedIn Kullanıcı Adı: {linkedin_target}",
                    f"LinkedIn Adı: {username}",
                    f"LinkedIn Pozisyon: {title}",
                    f"LinkedIn Şirket: {company}",
                    f"LinkedIn Süre: {duration}",
                    f"LinkedIn Lokasyon: {location}",
                    f"LinkedIn Açıklama: {description}",
                    f"LinkedIn Skills: {skills}",
                    "------------\n"
                ]
                output_lines.extend(section)

        # Twitter
        if twitter_username:
            driver.get(f"https://twitter.com/{twitter_username}")
            time.sleep(5)
            name = driver.find_element(By.XPATH, '//div[@data-testid="UserName"]//span').text if driver.find_elements(By.XPATH, '//div[@data-testid="UserName"]//span') else "Yok"
            bio = driver.find_element(By.XPATH, '//div[@data-testid="UserDescription"]').text if driver.find_elements(By.XPATH, '//div[@data-testid="UserDescription"]') else "Yok"
            joined = driver.find_element(By.XPATH, '//span[contains(text(), "Joined")]').text if driver.find_elements(By.XPATH, '//span[contains(text(), "Joined")]') else "Yok"
            followers = driver.find_element(By.XPATH, '//a[contains(@href,"/followers")]//span[1]').text if driver.find_elements(By.XPATH, '//a[contains(@href,"/followers")]//span[1]') else "Yok"
            following = driver.find_element(By.XPATH, '//a[contains(@href,"/following")]//span[1]').text if driver.find_elements(By.XPATH, '//a[contains(@href,"/following")]//span[1]') else "Yok"
            location = driver.find_element(By.XPATH, '//span[contains(@data-testid,"UserLocation")]').text if driver.find_elements(By.XPATH, '//span[contains(@data-testid,"UserLocation")]') else "Yok"
            website = driver.find_element(By.XPATH, '//span[contains(@data-testid,"UserUrl")]').text if driver.find_elements(By.XPATH, '//span[contains(@data-testid,"UserUrl")]') else "Yok"
            tweet = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text if driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]') else "Yok"

            twitter_section = [
                f"Twitter Kullanıcı Adı: {twitter_username}",
                f"Twitter İsim: {name}",
                f"Twitter Bio: {bio}",
                f"Twitter Lokasyon: {location}",
                f"Twitter Website: {website}",
                f"Twitter Katılım: {joined}",
                f"Twitter Takipçi: {followers}",
                f"Twitter Takip Edilen: {following}",
                f"Twitter Son Tweet: {tweet}",
                "------------\n"
            ]
            output_lines.extend(twitter_section)

    finally:
        if driver:
            driver.quit()

    # Instagram
    if instagram_username:
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
                f"Instagram Gönderi Sayısı: {profile.mediacount}",
                "------------\n"
            ]
            output_lines.extend(instagram_section)
        except Exception as e:
            output_lines.append(f"Instagram profil bilgileri çekilemedi: {e}")

    if not output_lines:
        messagebox.showinfo("Uyarı", "Lütfen en az bir platform bilgisi girin.")
        return

    with open("social_media_report.txt", "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")

    messagebox.showinfo("Tamamlandı", "Bilgiler 'social_media_report.txt' dosyasına kaydedildi.")

# GUI kurulum
top = tk.Tk()
top.title("Sosyal Medya Bilgi Toplayıcı")
top.geometry("400x400")

tk.Label(top, text="LinkedIn Hedef Kullanıcı:").pack()
entry_linkedin_target = tk.Entry(top, width=40)
entry_linkedin_target.pack()

tk.Label(top, text="Twitter Kullanıcı Adı:").pack()
entry_twitter_user = tk.Entry(top, width=40)
entry_twitter_user.pack()

tk.Label(top, text="Instagram Kullanıcı Adı:").pack()
entry_instagram_user = tk.Entry(top, width=40)
entry_instagram_user.pack()

tk.Button(top, text="Bilgileri Topla", command=run_script).pack(pady=10)

top.mainloop()
