import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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

        # Open login modal
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick='return showLogin();']")))
        login_btn.click()
        print("[INFO] Clicked login button")

        wait.until(EC.visibility_of_element_located((By.ID, "login_modal")))
        driver.execute_script("document.getElementById('login_modal_bg').remove();")
        print("[INFO] Login modal visible and overlay removed")

        login_modal = driver.find_element(By.ID, "login_modal")
        email_input = login_modal.find_element(By.NAME, "email")
        password_input = login_modal.find_element(By.NAME, "password")
        email_input.clear()
        email_input.send_keys(EMAIL)
        password_input.clear()
        password_input.send_keys(PASSWORD)

        login_submit = login_modal.find_element(By.XPATH, '//input[@type="submit" and @value="Log In"]')
        login_submit.click()
        print("[INFO] Login submitted")

        # CVV form
        wait.until(EC.presence_of_element_located((By.NAME, "cvc_existing")))
        cvv_input = driver.find_element(By.NAME, "cvc_existing")
        cvv_input.send_keys(CVV)

        print("[INFO] Attempting to purchase parking...")
        try:
            purchase_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @value="Purchase Parking"]')))
            purchase_btn.click()
            print("[INFO] Purchase button clicked")
        except:
            print("[WARN] Click failed. Submitting form directly...")
            driver.find_element(By.ID, "pay_form").submit()
            print("[INFO] Form submitted")

        print("[SUCCESS] Parking purchase flow completed!")
        time.sleep(3)  # Keep browser open briefly before closing

    except UnexpectedAlertPresentException:
        print("[ERROR] Unexpected alert during login:")
        try:
            alert = driver.switch_to.alert
            print("[ALERT] Text:", alert.text)
            alert.dismiss()
        except:
            print("[ERROR] Could not read alert text.")

    except Exception as e:
        print("[ERROR] Something went wrong:", str(e))

    finally:
        driver.quit()

# Run once for testing
purchase_parking()
