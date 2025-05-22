import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CVV = os.getenv("CVV")

def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def purchase_parking():
    print("[INFO] Starting parking automation...")
    driver = start_driver()
    driver.get("https://www.smrtpass.net/?z=1044")

    try:
        wait = WebDriverWait(driver, 15)

        # Click login link
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick='return showLogin();']")))
        login_btn.click()
        print("[INFO] Clicked login button")

        # Wait for modal
        wait.until(EC.visibility_of_element_located((By.ID, "login_modal")))
        print("[INFO] Login modal visible")

        # Remove overlay
        driver.execute_script("document.getElementById('login_modal_bg').remove();")
        print("[INFO] Removed modal overlay")
        driver.save_screenshot("modal_overlay_removed.png")

        # Login modal targeting
        print("[DEBUG] Getting login modal...")
        login_modal = driver.find_element(By.ID, "login_modal")

        print("[DEBUG] Locating email input in modal...")
        email_input = login_modal.find_element(By.NAME, "email")
        print("[DEBUG] Found email input. Typing email...")
        email_input.clear()
        email_input.send_keys(EMAIL)

        print("[DEBUG] Locating password input in modal...")
        password_input = login_modal.find_element(By.NAME, "password")
        print("[DEBUG] Found password input. Typing password...")
        password_input.clear()
        password_input.send_keys(PASSWORD)

        # Click login
        print("[INFO] Clicking actual Log In button...")
        login_submit = login_modal.find_element(By.XPATH, '//input[@type="submit" and @value="Log In"]')
        login_submit.click()
        print("[INFO] Login button clicked")

        # Wait for CVV field
        print("[INFO] Waiting for the purchase form or CVV input to load...")
        driver.save_screenshot("after_login.png")
        wait.until(EC.presence_of_element_located((By.NAME, "cvc_existing")))

        print("[INFO] Entering CVV...")
        cvv_input = driver.find_element(By.NAME, "cvc_existing")
        cvv_input.send_keys(CVV)

        # Click purchase button (with fallback)
        print("[INFO] Clicking Purchase Parking button...")
        driver.save_screenshot("before_purchase_click.png")

        try:
            purchase_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @value="Purchase Parking"]')))
            purchase_btn.click()
            print("[INFO] Clicked purchase button")
        except:
            print("[WARN] Click failed, attempting form submit() instead...")
            form = driver.find_element(By.ID, "pay_form")
            form.submit()
            print("[INFO] Form submitted directly")

        driver.save_screenshot("after_purchase_attempt.png")
        print("[SUCCESS] Parking purchase flow completed!")

        time.sleep(3)

    except UnexpectedAlertPresentException:
        print("[ERROR] Unexpected alert during login:")
        try:
            alert = driver.switch_to.alert
            print("[ALERT] Text:", alert.text)
            alert.dismiss()
        except:
            print("[ERROR] Could not read alert text.")
        driver.save_screenshot("alert_during_login.png")

    except Exception as e:
        print("[ERROR] Something went wrong:", str(e))
        driver.save_screenshot("error_debug.png")

    finally:
        driver.quit()

# Run once for testing
purchase_parking()
