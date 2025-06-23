import time, pytest, random
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
    # options.add_argument("--headless=new")  # 👈 Comment to see UI
    #options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_full_flow(driver):
    wait = WebDriverWait(driver, 20)
    driver.get(BASE_URL)
    print("🚀 Starting test")

    # Login
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    print("✅ Logged in")

    wait.until(EC.presence_of_element_located((By.ID, "dashboard-content")))

    # Navigate to Practice Test
    for item in driver.find_elements(By.CLASS_NAME, "sidebar-item"):
        if item.find_elements(By.CLASS_NAME, "fa-clipboard-list"):
            ActionChains(driver).move_to_element(item).perform()
            time.sleep(1)
            item.find_element(By.XPATH, ".//a[contains(text(),'Practice Test')]").click()
            break

    time.sleep(3)

    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        print("⚠️ Existing test detected. Attempting it.")

        for i in range(10):
            # Click question from left panel
            question_btns = driver.find_elements(By.CLASS_NAME, "question-item")
            if i < len(question_btns):
                driver.execute_script("arguments[0].click();", question_btns[i])
                time.sleep(1)

            # Choose random option (idx from 1 to 4)
            idx = random.randint(1, 4)
            try:
                option = driver.find_element(By.XPATH, f"//button[@class='option-button' and @idx='{idx}']")
                driver.execute_script("arguments[0].click();", option)
                print(f"✅ Q{i+1}: Selected option idx={idx}")
            except:
                print(f"⚠️ Q{i+1}: Option idx={idx} not found")

            time.sleep(1)

        # Submit
        submit_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "submit-button")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-button")))
        driver.execute_script("arguments[0].click();", submit_btn)

        for _ in range(2):
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print("🧾 Alert:", alert.text)
            alert.accept()
            time.sleep(1)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("🧹 Test submitted & tab closed")

    else:
        print("🆕 Creating new test")
        wait.until(EC.presence_of_element_located((By.ID, "NewTestFrame")))
        subject_select = Select(wait.until(EC.element_to_be_clickable((By.ID, "subject"))))
        subject_select.select_by_visible_text("Chemistry")
        wait.until(lambda d: d.find_element(By.ID, "grade").is_enabled())
        Select(driver.find_element(By.ID, "grade")).select_by_visible_text("10")

        topic_checkbox = wait.until(EC.element_to_be_clickable((By.ID, "checkbox-Acids,-Bases-and-Salts")))
        driver.execute_script("arguments[0].click();", topic_checkbox)
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.ID, "all-difficulty"))))
        driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.ID, "generateTest"))))

        wait.until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        for i in range(10):
            question_btns = driver.find_elements(By.CLASS_NAME, "question-item")
            if i < len(question_btns):
                driver.execute_script("arguments[0].click();", question_btns[i])
                time.sleep(1)

            idx = random.randint(1, 4)
            try:
                option = driver.find_element(By.XPATH, f"//button[@class='option-button' and @idx='{idx}']")
                driver.execute_script("arguments[0].click();", option)
                print(f"✅ Q{i+1}: Selected option idx={idx}")
            except:
                print(f"⚠️ Q{i+1}: Option idx={idx} not found")

            time.sleep(1)

        submit_btn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "submit-button")))
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-button")))
        driver.execute_script("arguments[0].click();", submit_btn)

        for _ in range(2):
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print("🧾 Alert:", alert.text)
            alert.accept()
            time.sleep(1)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("✅ Test completed and tab closed")

    # Logout
    for item in driver.find_elements(By.CLASS_NAME, "sidebar-item"):
        if item.find_elements(By.CLASS_NAME, "fa-sign-out-alt"):
            ActionChains(driver).move_to_element(item).perform()
            time.sleep(1)
            item.find_element(By.XPATH, ".//a[contains(text(),'Logout')]").click()
            break

    print("🔚 Logged out")
