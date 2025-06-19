import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ----------------------- CONFIG -----------------------
BASE_URL = "https://edupulse-qa.onrender.com/"

# ----------------------- DRIVER SETUP -----------------------
def create_driver():
    chrome_options = Options()
    # Uncomment below to run without browser window
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# ----------------------- HELPER: Login -----------------------
def perform_login(driver, username, password):
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dashboard-content")))
    print("✅ Logged in successfully")
    time.sleep(2)

# ----------------------- HELPER: Click Menu Item -----------------------
def click_menu(driver, label_text):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space()='{label_text}']"))
        )
        element.click()
        print(f"✅ Clicked on: {label_text}")
        time.sleep(1.5)
    except Exception as e:
        print(f"❌ Failed to click on '{label_text}': {e}")
        raise

# ----------------------- HELPER: Logout -----------------------
def perform_logout(driver):
    click_menu(driver, "Logout")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    print("✅ Logged out successfully")

# ----------------------- SINGLE FLOW TEST: Login → Menus → Logout -----------------------
def test_full_user_flow():
    driver = create_driver()
    try:
        perform_login(driver, "sarthak@tiet.com", "a")
        
        # Menu navigation
        for label in ["Practice Test", "History", "My Score Board", "Manage My Topics", "My Profile"]:
            click_menu(driver, label)

        print("✅ All menus verified.")

        # Logout
        perform_logout(driver)

    finally:
        driver.quit()

# ----------------------- MAIN: Run via CLI -----------------------
if __name__ == "__main__":
    pytest.main([__file__])
