import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def start_aternos_server():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/usr/bin/google-chrome"  # Adjust path if needed
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Ensure ChromeDriver is installed
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    ATERNOS_URL = "https://aternos.org/go/"
    ATERNOS_USERNAME = os.getenv("ATERNOS_USERNAME")
    ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

    driver.get(ATERNOS_URL)
    time.sleep(5)

    # Click on Login Button
    try:
        login_button = driver.find_element(By.XPATH, "//a[contains(@href, '/login/')]")
        login_button.click()
        time.sleep(3)
    except:
        print("⚠️ Login button not found. Maybe already logged in?")

    # Enter Username & Password
    driver.find_element(By.ID, "user").send_keys(ATERNOS_USERNAME)
    driver.find_element(By.ID, "password").send_keys(ATERNOS_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

    # Navigate to server page
    ATERNOS_SERVER_ID = os.getenv("ATERNOS_SERVER_ID")
    driver.get(f"https://aternos.org/server/#{ATERNOS_SERVER_ID}")
    time.sleep(3)

    logs = "Server logs:\n"

    # Click start button if found
     try:
    start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
    print("✅ Start button found. Clicking now...")
    start_button.click()
    time.sleep(10)
except:
    print("❌ Could not find the Start button! Server might already be running.")

    # Fetch logs
    try:
        log_elements = driver.find_elements(By.CLASS_NAME, "log-line")
        for log in log_elements:
            logs += log.text + "\n"
    except:
        logs += "⚠️ Couldn't retrieve logs.\n"

    driver.quit()
    return logs
