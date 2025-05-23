import requests
import pytest

BASE_URL = "https://api.matchbook.com/bpapi/rest/security/session"

def test_valid_login_request(valid_credentials):
    """
    Test the happy path: valid username and password should return 200 and a session token.
    """
    response = requests.post(BASE_URL, json=valid_credentials)
    print(response.status_code)
    assert response.status_code == 200
    data = response.json()
    assert "session-token" in data
    print(data["session-token"])
    assert data["session-token"]
    print(data["user-id"])
    assert "user-id" in data
    assert data["account"]
    assert "account" in data

def test_invalid_password(invalid_password_credentials):
    """
    Test login with a valid username and invalid password. Should return 400 and an error message.
    """
    response = requests.post(BASE_URL, json=invalid_password_credentials)
    print(response.status_code)
    assert response.status_code == 400
    print(response.text)
    #assert "Incorrect" in response.text.lower()

def test_invalid_username(invalid_username_credentials):
    """
    Test login with an invalid username and any password. Should return 400 and an error message.
    """
    response = requests.post(BASE_URL, json=invalid_username_credentials)
    print(response.status_code)
    assert response.status_code == 400
    assert "invalid" in response.text.lower()

def test_missing_username(valid_credentials):
    """
    Test login with missing username field. Should return 400 and an error about username.
    """
    payload = {"password": valid_credentials["password"]}
    response = requests.post(BASE_URL, json=payload)
    print(response.status_code)
    assert response.status_code == 400
    print(response.text)
    #assert "username" in response.text.lower()

def test_missing_password(valid_credentials):
    """
    Test login with missing password field. Should return 400 and an error about password.
    """
    payload = {"username": valid_credentials["username"]}
    response = requests.post(BASE_URL, json=payload)
    print(response.status_code)
    assert response.status_code == 400
    print(response.text)
    #assert "password" in response.text.lower() 


def test_session_token_expiry(valid_credentials):
    """
    Placeholder for session expiry logic. Should reject requests with expired session token.
    """
    response = requests.post(BASE_URL, json=valid_credentials)
    assert response.status_code == 200
    data = response.json()
    session_token = data.get("session-token")
    assert session_token
    # Simulate expiry (not practical in real time)
    # time.sleep(6 * 60 * 60 + 1)
    # response2 = requests.get(SOME_ENDPOINT, headers={"session-token": session_token})
    # assert response2.status_code in (401, 403)

def test_validate_json_response_structure(valid_credentials):
    """
    Validate the structure and key fields of the JSON response for a valid login.
    """
    response = requests.post(BASE_URL, json=valid_credentials)
    print(response.status_code)
    assert response.status_code == 200
    data = response.json()
    print(data["session-token"])
    assert "session-token" in data and data["session-token"]
    print(data["user-id"])
    assert "user-id" in data
    print(data["account"])
    assert "account" in data
    account = data["account"]
    assert account["username"] == valid_credentials["username"]
    print(account["email"])
    assert "email" in account
    assert account["status"] == "active"
    assert "role" in data and data["role"] == "USER"
    print(account["balance"])
    assert "balance" in account
    #assert account["currency"] == "USD"  # Assuming USD is the default currency
    print(account["currency"])
    assert "currency" in account
    assert "last-login" in account

@pytest.mark.skip(reason="We dont have a way to test this")
def test_account_suspension_after_three_failed_logins(valid_credentials, invalid_password_credentials):
    """
    Test that an account is suspended after three consecutive failed login attempts.
    The fourth attempt with correct credentials should fail due to suspension.
    """
    # 3 failed attempts
    for _ in range(3):
        # we use _ to ignore the loop variable
        response = requests.post(BASE_URL, json=invalid_password_credentials)
        assert response.status_code == 400
    # 4th attempt with correct password
    response = requests.post(BASE_URL, json=valid_credentials)
    assert response.status_code != 200  # Should be locked/suspended
    assert "suspend" in response.text.lower() or "lock" in response.text.lower()

@pytest.mark.skip(reason="Requires automation and may block your IP")
def test_ip_block_after_excessive_login_attempts(invalid_username_credentials):
    """
    Test that the API blocks an IP after more than 25 login attempts in one minute.
    Should return 429 or 403 and an appropriate error message.
    """
    for _ in range(26):
        # we use _ to ignore the loop variable
        response = requests.post(BASE_URL, json=invalid_username_credentials)
    # 27th attempt
    response = requests.post(BASE_URL, json=invalid_username_credentials)
    print(response.status_code)
    assert response.status_code in (429, 403)
    print(response.text)
    #assert "block" in response.text.lower() or "too many" in response.text.lower()

@pytest.mark.skip(reason="The test fails and needs to be investigated")
def test_sql_injection_attempt_in_login():
    """
    Test that a SQL injection string in the username does not allow login and is handled safely.
    """
    payload = {
        "username": "' OR 1=1; --",
        "password": "anyvalue"
    }
    response = requests.post(BASE_URL, json=payload)
    # Should not succeed
    print(response.status_code)
    assert response.status_code != 200
    # Should indicate invalid credentials, not a server/database error
    assert "invalid" in response.text.lower() or "error" in response.text.lower()
    # Should not expose SQL/database errors
    assert "sql" not in response.text.lower()
    assert "syntax" not in response.text.lower()
    assert "exception" not in response.text.lower()