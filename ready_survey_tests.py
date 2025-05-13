# ready_survey_tests.py
# ---------------------------------------------------------------
# Selenium tests for the “ready survey” HTML form
# ---------------------------------------------------------------
# Run with:  python ready_survey_tests.py
# ---------------------------------------------------------------
import time, datetime as dt
import chromedriver_autoinstaller
results = []   
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

ROOT       = "http://127.0.0.1:5000"
FORM_PATH  = "/survey/form"
LOGIN_URL  = "/auth/login"


class ReadySurveyTest:
    # ------------------------------------------------------------
    def __init__(self, root):
        chromedriver_autoinstaller.install()
        opts = webdriver.ChromeOptions()
        opts.add_argument("--ignore-certificate-errors")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(5)
        self.root = root
        print("[✔] Chrome driver started.")

    def __del__(self):
        try:
            self.driver.quit()
            print("[✘] Chrome driver stopped.")
        except Exception:
            pass
    # ------------------------------------------------------------
    # helper utilities
    def _flash_message(self):
        try:
            ele = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".alert"))
            )
            return ele.text.strip(), ele.get_attribute("class")
        except TimeoutException:
            return "", ""

    def _fill_text(self, name: str, value: str):
        box = self.driver.find_element(By.NAME, name)
        box.clear()
        box.send_keys(value)

    def _click_checkbox(self, model: str):
        """
        Tick the AI-model checkbox whose VALUE matches the model name.
        HTML pattern: <input name="ai_models" value="ChatGPT" …>
        """
        cb = self.driver.find_element(
            By.CSS_SELECTOR, f"input[name='ai_models'][value='{model}']"
        )
        if not cb.is_selected():
            cb.click()
    # ------------------------------------------------------------
    # public API
    def login(self, email: str, password: str) -> bool:
        self.driver.get(self.root + LOGIN_URL)
        self._fill_text("email_or_phone", email)
        self._fill_text("password", password)
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(1.2)                       # tiny wait for redirect
        logged_in = LOGIN_URL not in self.driver.current_url
        print("[+] Logged-in." if logged_in else "[-] Login failed.")
        return logged_in

    def open_form(self):
        self.driver.get(self.root + FORM_PATH)

    def submit_ready_survey(self, title: str, payload: dict, *, expect_success=True):
        print(f"\n[TEST] {title}")
        self.open_form()

        # ------------ fill static fields -------------------------
        self._fill_text("name",      payload.get("name", ""))
        self._fill_text("surname",   payload.get("surname", ""))
        self._fill_text("birthDate", payload.get("birthDate", ""))
        self._fill_text("useCase",   payload.get("useCase", ""))

        Select(self.driver.find_element(By.NAME, "educationLevel"))\
            .select_by_visible_text(payload.get("educationLevel", ""))
        self._fill_text("city", payload.get("city", ""))
        Select(self.driver.find_element(By.NAME, "gender"))\
            .select_by_visible_text(payload.get("gender", ""))

        # ------------ AI models & dynamic defect boxes ----------
        for model, text in payload.get("defects", {}).items():
            self._click_checkbox(model)

            try:
                defect_box = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located((By.NAME, f"defect_{model}"))
                )
                if text:
                    defect_box.send_keys(text)
            except TimeoutException:
                pass  # fine if 'None' was chosen

        # ------------ submit & assert ---------------------------
        # --- make sure the button is visible, then click it safely ----------
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(submit_btn))
        # use JS click to avoid interception by sticky footers / overlays
        self.driver.execute_script("arguments[0].click();", submit_btn)
        msg, klass = self._flash_message()
        ok = "alert-success" in klass
        print(f"[=] Browser reported: {'SUCCESS' if ok else 'FAILURE'} – «{msg}»")
        results.append((title, ok == expect_success))   
        assert ok == expect_success
    # ------------------------------------------------------------


# ----------------------------------------------------------------
# TEST RUNNER
# ----------------------------------------------------------------
def main():
    t = ReadySurveyTest(ROOT)
    if not t.login("imredamla9@gmail.com", "12345678"):
        return

    today   = dt.date.today()
    future  = (today + dt.timedelta(days=1)).isoformat()

    # 1. Happy path
    t.submit_ready_survey("Valid submission", {
        "name": "John", "surname": "Doe", "birthDate": "1990-06-15",
        "educationLevel": "High School", "city": "Ankara", "gender": "Male",
        "defects": {"ChatGPT": "Sometimes hallucinates"},
        "useCase": "Academic research"
    }, expect_success=True)

    # 2. Missing name
    t.submit_ready_survey("Missing name", {
        "name": "", "surname": "Doe", "birthDate": "1990-06-15",
        "educationLevel": "High School", "city": "Ankara", "gender": "Female",
        "defects": {"ChatGPT": "Latency"}, "useCase": "Testing"
    }, expect_success=False)

    # 3. Future birth date
    t.submit_ready_survey("Birth date in the future", {
        "name": "Jane", "surname": "Doe", "birthDate": future,
        "educationLevel": "High School", "city": "Ankara", "gender": "Female",
        "defects": {"Bard": "Incorrect answers"}, "useCase": "Fun"
    }, expect_success=False)

    # 4. No AI model selected
    t.submit_ready_survey("No AI model", {
        "name": "Alice", "surname": "Smith", "birthDate": "1985-01-01",
        "educationLevel": "Master’s", "city": "İstanbul", "gender": "Female",
        "defects": {}, "useCase": "Personal"
    }, expect_success=False)

    # 5. ‘None’ mixed with another model
    t.submit_ready_survey("'None' with another model", {
        "name": "Bob", "surname": "Brown", "birthDate": "1992-03-10",
        "educationLevel": "High School", "city": "Ankara", "gender": "Male",
        "defects": {"None": "—", "Claude": "Too verbose"}, "useCase": "Business"
    }, expect_success=False)

    # 6. Model selected but defect empty
    t.submit_ready_survey("Empty defect description", {
        "name": "Charlie", "surname": "Green", "birthDate": "1994-07-22",
        "educationLevel": "PhD", "city": "İzmir", "gender": "Male",
        "defects": {"Copilot": ""}, "useCase": "Development"
    }, expect_success=False)
    print("\n========== SUMMARY ==========")
    for title, passed in results:
        print(f"{title:30} : {'PASS' if passed else 'FAIL'}")
    print("================================")



if __name__ == "__main__":
    main()
