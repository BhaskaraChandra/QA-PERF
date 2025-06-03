To use Selenium WebDriver and Pytest, you'll need to install the following:

1. Python
- Make sure you have Python installed on your system (preferably the latest version).

2. Selenium WebDriver
- Install the Selenium WebDriver library using pip: pip install selenium

3. Pytest
- Install Pytest using pip: pip install pytest

4. WebDriver Executable
- You'll need to download the WebDriver executable for the browser you want to test (e.g., ChromeDriver for Chrome, GeckoDriver for Firefox).
- Make sure the executable is in your system's PATH or provide the path to the executable when creating the WebDriver instance.

Optional
- You can also install additional libraries, such as:
    - pytest-html for generating HTML reports: pip install pytest-html
    - pytest-xdist for parallel testing: pip install pytest-xdist

Verify Installation
- Open a terminal or command prompt and run pytest --version to verify Pytest installation.
- Run python -c "import selenium" to verify Selenium WebDriver installation.

With these installations, you're ready to start using Selenium WebDriver and Pytest for your test automation needs.