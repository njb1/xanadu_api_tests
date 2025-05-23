import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

LOGIN_URL = "https://www.matchbook.com/login"
# In real code, use env vars or something like AWS Secrets Manager
# or HashiCorp Vault to store sensitive data
YOUR_VALID_USERNAME = "YOUR_VALID_USERNAME"
YOUR_VALID_PASSWORD = "YOUR_VALID_PASSWORD"
YOUR_WRONG_PASSWORD = "YOUR_WRONG_PASSWORD"
INVALID_USERNAME = "INVALID_USER"

# Note: this is a placeholder for your actual username and password.
# This is largely untested as I didnt think it was a good idea to test agaianst a live site


def login(driver, username, password):
    driver.get(LOGIN_URL)
    # Accept all cookies if the button is present
    try:
        accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All Cookies')]")
        accept_btn.click()
        time.sleep(1)
    except Exception:
        pass

    time.sleep(5)

    # this was originally in the function but thought it could be reused
    close_any_popup(driver)

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)

    time.sleep(3)

    # Try by data-hook first, then <a> text, then <button>, then absolute XPath as fallback
    try:
        driver.find_element(By.CSS_SELECTOR, "a[data-hook='loginbutton']").click()
    except Exception:
        try:
            driver.find_element(By.XPATH, "//a[contains(text(),'Login')]").click()
        except Exception:
            try:
                driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
            except Exception:
                # Fallback to absolute XPath if needed
                driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]/div/div[1]/div[2]/span/div/form/div[2]/a[1]").click()

def test_valid_login(driver):
    """
    Test Case 1: Valid Login.
    """
    login(driver, YOUR_VALID_USERNAME, YOUR_VALID_PASSWORD)
    time.sleep(3)
    assert "account" in driver.page_source.lower() or "dashboard" in driver.current_url.lower()

def test_invalid_password(driver):
    """
    Test Case 2: Invalid Password.
    """
    login(driver, YOUR_VALID_USERNAME, YOUR_WRONG_PASSWORD)
    time.sleep(2)
    assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower()

def test_invalid_username(driver):
    """
    Test Case 3: Invalid Username.
    """
    login(driver, INVALID_USERNAME, YOUR_VALID_PASSWORD)
    time.sleep(2)
    assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower()

def test_empty_username_and_password(driver):
    """
    Test Case 4: Empty Username and Password
    """
    driver.get(LOGIN_URL)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.XPATH, "//a[contains(text(),'Login')]").click()
    time.sleep(1)
    assert "required" in driver.page_source.lower() or "enter" in driver.page_source.lower()

@pytest.mark.skip(reason="Password field masking is a visual/UI feature and may not be reliably tested in automation.")
def test_password_field_masking(driver):
    """
    Test Case 5: Password Field Masking.
    """
    driver.get(LOGIN_URL)
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("sometext")
    assert password_field.get_attribute("type") == "password"
    # Optionally check for 'eye' icon to show password
    eye_icons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Show password')]")
    assert eye_icons

@pytest.mark.skip(reason="Session timeout is not practical to automate in real time")
def test_session_timeout(driver):
    """
    Test Case 6: Session Timeout.
    """
    login(driver, "YOUR_VALID_USERNAME", "YOUR_VALID_PASSWORD")
    # Wait for session timeout (e.g., 6 hours) - not practical for automation
    # time.sleep(6 * 60 * 60)
    # assert "login" in driver.current_url.lower() or "expired" in driver.page_source.lower()
    pass

@pytest.mark.skip(reason="Remember Me not present or not automatable")
def test_remember_me_functionality(driver):
    """
    Test Case 7: Remember Me Functionality.
    """
    # If 'Remember Me' is present, automate checking the box and browser restart
    pass

@pytest.mark.skip(reason="Probably not a good idea to test against a live site")
def test_sql_injection_attempt(driver):
    """
    Test Case 8: SQL Injection Attempt in Login.
    """
    login(driver, "' OR 1=1; --", "anyvalue")
    time.sleep(2)
    login(driver, "' OR 1=1; --", "anyvalue")
    time.sleep(2)
    assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower()
    assert "sql" not in driver.page_source.lower()
    assert "exception" not in driver.page_source.lower()

@pytest.mark.skip(reason="Again, probably not a good idea to test against a live site")
def test_username_password_length_boundaries(driver):
    """
    Test Case 9: Username and Password Field Length Boundaries
    """
    min_length = 1
    max_length = 50  # Adjust as per actual requirements

    # Minimum username
    login(driver, "a" * min_length, YOUR_VALID_PASSWORD)
    time.sleep(1)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()

    # Maximum username
    login(driver, "a" * max_length, YOUR_VALID_PASSWORD)
    time.sleep(1)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()

    # Exceed maximum username
    login(driver, "a" * (max_length + 1), YOUR_VALID_PASSWORD)
    time.sleep(1)
    assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower() or "length" in driver.page_source.lower()
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()

    # Minimum password
    login(driver, YOUR_VALID_USERNAME, "a" * min_length)
    time.sleep(1)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()

    # Maximum password
    login(driver, YOUR_VALID_USERNAME, "a" * max_length)
    time.sleep(1)
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()

    # Exceed maximum password
    login(driver, YOUR_VALID_USERNAME, "a" * (max_length + 1))
    time.sleep(1)
    assert "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower() or "length" in driver.page_source.lower()
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()

def close_any_popup(driver, timeout=3):
    """
    Attempts to close any popup/modal that may appear after page load.
    Tries several common selectors for close buttons or 'x' icons.
    Only clicks if the element is visible and interactable.
    """
    close_selectors = [
        "//button[contains(@aria-label, 'Close')]",
        "//button[contains(text(), 'Close')]",
        "//button[contains(@class, 'close')]",
        "//button[.//span[text()='×'] or .//span[text()='x']]",
        "//button[.='×']",
        "//button[.='x']"
    ]
    for selector in close_selectors:
        try:
            close_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            close_button.click()
            time.sleep(1)
            break
        except Exception:
            continue

def accept_all_cookies(driver):
    """
    Attempts to accept all cookies if the 'Accept All Cookies' button is present.
    Can be reused in any test that needs to handle the cookie consent popup.
    """
    try:
        accept_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All Cookies')]")
        accept_btn.click()
        time.sleep(1)
    except Exception:
        pass