from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import chromedriver_autoinstaller
import time

class Test:
    def __init__(self, domain):
        try:
            chromedriver_autoinstaller.install()

            options = webdriver.ChromeOptions()
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--allow-insecure-localhost")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(5)

            print(f"[INFO] Navigating to: {domain}")
            self.driver.get(domain)
            print("[✔] Chrome driver initiated and page loaded.")
        except TimeoutException as te:
            print("Error:", te)

    def __del__(self):
        self.driver.quit()
        print("[✘] Chrome driver stopped.")

    def login(self, email, password):
        self.driver.get("http://127.0.0.1:5000/auth/login")
        time.sleep(1)

        try:
            email_input = self.driver.find_element(By.ID, "email_or_phone")
            email_input.clear()
            email_input.send_keys(email)
            print("[+] Email entered.")
        except NoSuchElementException:
            print("[-] Email input not found.")
            return False

        try:
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(password)
            print("[+] Password entered.")
        except NoSuchElementException:
            print("[-] Password input not found.")
            return False

        try:
            login_btn = self.driver.find_element(By.ID, "submit")
            login_btn.click()
            print("[+] Login button clicked.")
            time.sleep(2)
            return True
        except NoSuchElementException:
            print("[-] Login button not found.")
            return False

    def test_create_survey(self, title, questions):
        self.driver.get("http://127.0.0.1:5000/custom-survey/designer")
        time.sleep(1)

        # Fill Title
        try:
            title_input = self.driver.find_element(By.NAME, "title")
            time.sleep(1.5)
            title_input.clear()
            title_input.send_keys(title)
            print("[+] Survey title entered.")
        except NoSuchElementException:
            print("[-] Survey title input not found.")
            return

        for i, q in enumerate(questions):
            time.sleep(1.5)
            try:
                # Click "Add Question" button
                add_btn = self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", add_btn)

                WebDriverWait(self.driver, 5).until(
                    lambda driver: len(driver.find_elements(By.CLASS_NAME, "question-block")) > num_before
                )
                question_blocks = self.driver.find_elements(By.CLASS_NAME, "question-block")
                block = question_blocks[-1]

                # Fill question text
                block.find_element(By.CSS_SELECTOR, ".q-text").send_keys(q["text"])
                time.sleep(1.5)

                # Select question type
                select = Select(block.find_element(By.CSS_SELECTOR, ".form-select"))
                select.select_by_visible_text(q["type"])
                time.sleep(1.5)

                # Fill options if necessary
                if q["type"] != "Open Text":
                    time.sleep(1.5)
                    options_input = block.find_element(By.CSS_SELECTOR, ".q-options .form-control")
                    options_input.send_keys(",".join(q.get("options", [])))

                # Check "required" if true
                if q.get("required", False):
                    time.sleep(1.5)
                    checkbox = block.find_element(By.CSS_SELECTOR, ".q-required")
                    if not checkbox.is_selected():
                        checkbox.click()

                # Conditional logic if given
                if "conditional" in q:
                    time.sleep(1.5)
                    block.find_element(By.CSS_SELECTOR, ".cond-qid").send_keys(q["conditional"].get("question", ""))
                    block.find_element(By.CSS_SELECTOR, ".cond-val").send_keys(q["conditional"].get("value", ""))

                print(f"[+] Question {i} added successfully.")

            except Exception as e:
                print(f"[-] Error on question {i}: {e}")
                return

        # Save survey
        try:
            save_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_btn)
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", save_btn)
            print("[+] Survey saved.")
            time.sleep(1.5)
            
        except Exception as e:
            print("[-] Save Survey button not clickable:", e)
