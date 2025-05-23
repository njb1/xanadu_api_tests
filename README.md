# Xanadu API & UI QA Challenge

This repository contains manual and automated tests for the Matchbook login API, as part of the Xanadu QA challenge. The focus is on demonstrating manual QA, but also UI automation, and API automation skills.

How I approached this:
The login request sends as part of its body (the json blob) the username and password, there
are variations on how these can be sent, both valid, one or the other invalid etc.
One we have posted these, we look at the response body to determine the status (200 for success). The response body also has other information which we can verify. Outside of the scope of this project we should check the values against the database.
In addition we check for the user trying to do something they shouldnt, for example sql injection.
For the manual tests I have broke the steps into Postman and Insomnia (running the show_me_the_manual_api_steps.py will give you the option for both).

As an aside, I used Copilot to help write the show_me_the_manual_api_steps.py file. Although I aggree that the 80/20 rule still applies for AI enerated code, its worth exploring.

As partner tests to the manual API tests, I created UI specific tests to compliment them (both manual and via Selenium). These are mostly untested as I didnt think it a good idea to run tests against a live site.

I have created a traxability matrix to show how we cover the feature. This was my first time
creating a tracability matrix so I hope it ok.

I also created a dummy jenkinsfile.new to show how we might run this on the pipline.

---

## 📂 Repository Structure

- `xanadu_manual_api.txt`  
  High-level manual API test cases.

- `xanadu_manual_api_detailed.txt`  
  Step-by-step instructions for running each manual API test in Postman and Insomnia.

- `test/xanadu_automated_api.py`  
  Automated API tests using Python and pytest.

- `test/xanadu_automated_ui.py`  
  Automated UI tests using Selenium and pytest.

- `conftest.py`  
  Shared pytest fixtures for test data and configuration.

---

## 🚀 How to Run Automated Tests

### 1. Install dependencies  
Make sure you have Python installed.

For API tests:
```
pip install pytest requests
```

For UI tests (Selenium):
```
pip install pytest selenium
```
You will also need a WebDriver (e.g., ChromeDriver) available in your PATH (this can depend on your VPN settings).

---

### 2. Configure credentials  
Update the valid username and password in `conftest.py` and/or `test/xanadu_automated_ui.py` with your test account.

---

### 3. Run all tests

**Run all API and UI tests:**
```
pytest
```

**Run only API tests:**
```
pytest test/xanadu_automated_api.py
```

**Run only UI tests:**
```
pytest test/xanadu_automated_ui.py
```

---

### 4. Run a single test

**Run a specific test function by name (API or UI):**
```
pytest test/xanadu_automated_api.py -k test_valid_login
```
or
```
pytest test/xanadu_automated_ui.py -k test_valid_login
```

You can also run a specific test by its node id:
```
pytest test/xanadu_automated_api.py::test_valid_login
```
or
```
pytest test/xanadu_automated_ui.py::test_valid_login
```

---

## 🧪 Manual API Testing

See `xanadu_manual_api_detailed.txt` for step-by-step instructions to run each test case using Postman or Insomnia.

---

## 📖 How to Run the Manual API Steps Navigator

You can use the `show_me_the_manual_api_steps.py` script to interactively view step-by-step manual API test instructions for either Postman or Insomnia.

### Steps:

1. **Navigate to the `src` directory** (or wherever the script is located):
    ```
    cd src
    ```

2. **Run the script with Python:**
    ```
    python show_me_the_manual_api_steps.py
    ```

3. **Follow the prompts:**
    - Enter `p` for Postman steps or `i` for Insomnia steps.
    - Use `n` to go to the next test, `b` to go back, and `q` to quit.

> **Note:**  
> Make sure `xanadu_manual_api_detailed.txt` is in the same directory as the script, or adjust the script to point to the correct path.

---

## 🛡️ Security Test Example

Automated and manual tests include a SQL injection attempt to ensure the API is not vulnerable to common injection attacks.

---

## 📋 Notes

- Some tests (e.g., account lockout, IP blocking) are marked as skipped or require special setup.
- Do not commit real credentials to version control (seriously, dont!).

---

## 📊 Traceability Matrix

A traceability matrix is included in `src/tracability_matrix.txt`.  
This matrix maps each requirement or feature to its corresponding API and UI test cases, helping ensure complete test coverage and making it easy to see which tests validate which requirements.

---

## 🏗️ Jenkins Pipeline Example

A sample Jenkins pipeline configuration is provided in `jenkinsfile.new`.  
This file demonstrates how you might automate the running of both API and UI tests in a CI/CD pipeline using Jenkins. It includes steps for installing dependencies, running tests, and handling results and notifications. Just a sample as we dont have a pipelint to run it against.

---

Feel free to checkout a new branch and submit pull requests with improvements or additional tests.

---

## 🤝 Contributing

If this was on GitHub you would be able to checkout a new branch and submit pull requests with improvements or additional tests.

---

## 🛠️ Common Git Commands

Here are some useful git commands for working with repositories:

- **Clone the repository:**
  ```
  git clone https://github.com/your-org/the_repo.git
  ```

- **Check the status of your working directory:**
  ```
  git status
  ```

- **Create and switch to a new branch:**
  ```
  git checkout -b my-feature-branch
  ```

- **Add changes to staging:**
  ```
  git add . (. for all or just put the filenames)
  ```

- **Commit your changes:**
  ```
  git commit -m "Describe your changes"
  ```

- **Push your branch to the remote repository:**
  ```
  git push origin my-feature-branch
  ```

- **Pull the latest changes from the main branch:**
  ```
  git pull origin main
  ```

- **Merge another branch into your current branch:**
  ```
  git merge branch-name
  ```

- **Fetch all branches and tags from the remote:**
  ```
  git fetch --all
  ```

- **See your commit history:**
  ```
  git log --oneline --graph --all
  ```

---

## 📧 Contact

For questions about this repo, please contact the Xanadu QA team or me.