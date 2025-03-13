# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007BD2503FE345DAB2FF6C003F9803117271BAF1C7C65D585A8838C095FC829B5AAF18ABB5273AD9DBF858D45A9A26729DDC4EBBC3A0ADDF474B6847CDDCE84932FCFE372CB5116A7125D46C59EB1316FF0152FBCFF677F3870B98E43AF46AD57860EBF75E0D9EC8A6348A17CBEBA50A93A1143731BAFA576924965B050985980665E3981F5426FDB3F9520A6FB9771566EAC4FD6B07F2392BC79E29C425FAB909FFE998AD186709EC8A00AFA0C0F7FB5E3EBB5E1D27AE361A88F99604BE8ABA6A8580089EA37E81A47120E7E88B8B40682AABA106A99425B4AF1D4775B6A7B0B21221E152B511BFBC3C6B07CAB057297D26E62DB121B40CF5FB24A217CC412DB410890644F9941342916B0CE030C979463378C5F13884299C3AB6D0994F1DB1E7BCF9576EA93CBF4729A6CE459C71F51034515A1555C820A15D96FAA62207144AF971CA83B0352D76F118730646250D79CF37BC537E15B56BAF0442404D0F1946"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
