from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

class Test:
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    driver = webdriver.Chrome(options=options)
    def __init__(self, domain):
        try:
            self.driver.implicitly_wait(5)
            self.driver.get(domain)
            print("[!] Chrome driver initiated...")
        except TimeoutException as te:
            print("Error:", te)

    def __del__(self):
        self.driver.quit()
        print("[!] Chrome driver stopped...")