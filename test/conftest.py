import pytest
from selenium import webdriver


BASE_URL = "https://api.matchbook.com/bpapi/rest/security/session"
VALID_USERNAME = "xxx"
VALID_PASSWORD = "xxx"  # In real code, use env vars or something like aws_secrets
# or vault to store sensitive data
INVALID_USERNAME = "INVALID_USER"
INVALID_PASSWORD = "wrong_password"


@pytest.fixture
def valid_credentials():
    return {"username": VALID_USERNAME, "password": VALID_PASSWORD}

@pytest.fixture
def invalid_password_credentials():
    return {"username": VALID_USERNAME, "password": INVALID_PASSWORD}

@pytest.fixture
def invalid_username_credentials():
    return {"username": INVALID_USERNAME, "password": VALID_PASSWORD}

@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Or use webdriver.Firefox() or whatever
    driver.implicitly_wait(10)
    yield driver
    driver.quit()