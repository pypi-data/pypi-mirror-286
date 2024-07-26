from retrying import retry
from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class Selenium:
    def __init__(self):
        self.x = False

    @staticmethod
    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def get_browser(headless=True):
        options = Options()
        if headless == True:
            options.add_argument("--headless")

        return webdriver.Chrome(options=options)

    @staticmethod
    def get_element(browser, element_xpath, delay=10):
        if delay == None:
            return browser.find_element("xpath", element_xpath)
        try:
            element = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.XPATH, element_xpath))
            )
            return element
        except TimeoutException:
            print("Loading took too much time!")
            raise Exception("Timeout in first load")
