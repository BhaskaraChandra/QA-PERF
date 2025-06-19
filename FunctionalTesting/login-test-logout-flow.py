import time, pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://edupulse-qa.onrender.com/"
USERNAME = "sarthak@tiet.com"
PASSWORD = ""

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")  # ✅ Modern headless mode
    options.add_argument("--disable-gpu")   # (optional but recommended on Windows)
    options.add_argument("--window-size=1920,1080")  # ensures consistent layout rendering

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


def test_full_flow(driver):
    wait = WebDriverWait(driver, 20)
    print("🚀 Starting test: Navigating to login page")
    driver.get(BASE_URL)

    # Login
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    print("✅ Logged in successfully")
    # Wait for dashboard
    wait.until(EC.presence_of_element_located((By.ID, "dashboard-content")))

    # Sidebar hover > Assessments > Practice Test
    for item in driver.find_elements(By.CLASS_NAME, "sidebar-item"):
        if item.find_elements(By.CLASS_NAME, "fa-clipboard-list"):
            ActionChains(driver).move_to_element(item).perform()
            time.sleep(1)
            item.find_element(By.XPATH, ".//a[contains(text(),'Practice Test')]").click()
            break

    # Wait briefly to detect if an existing test window opened
    time.sleep(3)

    if len(driver.window_handles) > 1:
        # ⚠️ Existing test resumed in new tab
        driver.switch_to.window(driver.window_handles[-1])
        print("⚠️ Detected existing test. Submitting it directly.")

        # Submit directly
        submit_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submit-button"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-button")))
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(2)

        # Handle 2 browser alerts
        for _ in range(2):
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print("Alert says:", alert.text)
            alert.accept()
            time.sleep(2)

        # Close test tab and switch back
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("🧹 Test tab closed. Returned to dashboard")

    else:
        # ✅ Proceed with new test creation
        print("🆕 Creating new test from scratch")
        wait.until(EC.presence_of_element_located((By.ID, "NewTestFrame")))

        # Select subject = Chemistry
        print("➡️ Selecting subject: Chemistry")
        subject_select = Select(wait.until(EC.element_to_be_clickable((By.ID, "subject"))))
        subject_select.select_by_visible_text("Chemistry")

        # Wait until grade dropdown is enabled
        wait.until(lambda d: d.find_element(By.ID, "grade").is_enabled())

        # Select grade = 10 (fixed)
        print("➡️ Selecting grade: 10")
        grade_select = Select(driver.find_element(By.ID, "grade"))
        grade_select.select_by_visible_text("10")

        # Select topic: Acids, Bases and Salts
        print("➡️ Selecting topic and difficulty")
        topic_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "checkbox-Acids,-Bases-and-Salts")))
        driver.execute_script("arguments[0].click();", topic_checkbox)

        # Select All difficulty levels
        select_all_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "all-difficulty")))
        driver.execute_script("arguments[0].click();", select_all_checkbox)

        # Click Generate Test
        print("🧪 Generating the test")
        generate_btn = wait.until(EC.element_to_be_clickable((By.ID, "generateTest")))
        driver.execute_script("arguments[0].click();", generate_btn)

        # Switch to new test tab
        wait.until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])
        print("🪟 New test tab opened. Submitting test")

        # Submit directly without answering
        submit_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "submit-button")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-button")))
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(3)

        # Handle alerts
        for _ in range(2):
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print("Alert says:", alert.text)
            alert.accept()
            time.sleep(2)

        # Close tab and return
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("🧹 Test tab closed. Returned to dashboard")

    # Logout
    print("🔚 Logging out")
    for item in driver.find_elements(By.CLASS_NAME, "sidebar-item"):
        if item.find_elements(By.CLASS_NAME, "fa-sign-out-alt"):
            ActionChains(driver).move_to_element(item).perform()
            time.sleep(1)
            item.find_element(By.XPATH, ".//a[contains(text(),'Logout')]").click()
            break

    time.sleep(2)
