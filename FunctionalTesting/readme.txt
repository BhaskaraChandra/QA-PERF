Yes, there are several Python frameworks that can help you with functional testing of a web application. Here are some popular ones:

1. Selenium WebDriver
- A widely-used tool for automating web browsers.
- Supports multiple programming languages, including Python.
- Can be used for functional testing, regression testing, and more.

2. Pytest
- A popular testing framework for Python.
- Can be used for functional testing, unit testing, and integration testing.
- Supports fixtures, parametrization, and more.

3. Behave
- A BDD (Behavior-Driven Development) framework for Python.
- Allows you to write tests in natural language.
- Supports functional testing and integration testing.

4. Pytest-BDD
- A Pytest plugin for BDD testing.
- Allows you to write tests in natural language.
- Supports functional testing and integration testing.

5. Robot Framework
- A generic test automation framework.
- Supports functional testing, acceptance testing, and more.
- Has a large ecosystem of libraries and tools.

Example with Selenium WebDriver and Pytest
Here's an example of using Selenium WebDriver with Pytest:

import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login(driver):
    driver.get("https://example.com/login")
    driver.find_element_by_name("username").send_keys("username")
    driver.find_element_by_name("password").send_keys("password")
    driver.find_element_by_name("login").click()
    assert driver.title == "Login Success"

These frameworks can help you write functional tests for your web application, ensuring it works as expected from a user's perspective.