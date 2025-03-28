import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def start_aternos_server():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chrome_options)

    ATERNOS_URL = "https://aternos.org/go/"
    ATERNOS_USERNAME = os.getenv("ATERNOS_USERNAME")
    ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

    driver.get(ATERNOS_URL)
    time.sleep(3)

    # Login to Aternos
    driver.find_element(By.ID, "user").send_keys(ATERNOS_USERNAME)
    driver.find_element(By.ID, "password").send_keys(ATERNOS_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(5)

    # Navigate to server page
    ATERNOS_SERVER_ID = os.getenv("ATERNOS_SERVER_ID")
    driver.get(f"https://aternos.org/server/#{ATERNOS_SERVER_ID}")
    time.sleep(3)

    # Click start if server is offline
    logs = "Server logs:\n"
    try:
        start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
        start_button.click()
        time.sleep(5)
        logs += "✅ Server start request sent.\n"
    except:
        logs += "⚠️ Server is already online or button not found.\n"

    # Fetch logs (Example: Adjust XPath if needed)
    try:
        log_elements = driver.find_elements(By.CLASS_NAME, "log-line")
        for log in log_elements:
            logs += log.text + "\n"
    except:
        logs += "⚠️ Couldn't retrieve logs.\n"

    driver.quit()
    return logs
  
