
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

print("LoginTest")
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    #driver.quit()

def test_login(driver):
    print("LoginTest")
    driver.get("https://edupulse-qa.onrender.com/")
    driver.find_element("name","username").send_keys("sarthak@tiet.com")
    #driver.find_element("name","password").send_keys("a")
    #driver.find_element("name","Login").click()
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

    time.sleep(60)
    assert driver.title == "User Dashboard"
