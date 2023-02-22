from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.wait import WebDriverWait

import helper_tests

INET_SITE = "https://www.inet.se/"

class TestClass:
    @pytest.fixture(scope="class")
    def load_driver(self):

        driver = webdriver.Chrome()

        yield driver

        print('RUN CLASS TEARDOWN')

        driver.quit()

    @pytest.fixture
    def get_inet_site(self, load_driver):

        driver = load_driver

        driver.get(INET_SITE)

        cookies_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/button[1]")
        cookies_button.click()

        yield driver

        print('RUN TEST TEARDOWN')

        driver.delete_all_cookies()
        
    def test_1(self, get_inet_site):
        driver = get_inet_site

        helper_tests.boolean_assert("inet" in driver.current_url, f"Expected inet in url, got: {driver.current_url}")
    
    def test_advanced_2(self, get_inet_site):
        driver = get_inet_site

        datorer_link = driver.find_element(By.XPATH, '//*[@id="react-root"]/div[3]/div/div/div[2]/div[2]/div[3]/div/a[1]/div')

        datorer_link.click()

        h1 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h1"))
        expected_h1 = "Datorer"

        helper_tests.boolean_assert(expected_h1 in h1.text, f"Expected {expected_h1} in text for h1, got: {h1.text}")

        expected_title = "Datorer - Köp online här"

        helper_tests.boolean_assert(expected_title in driver.title, f"Expected {expected_title} in title, got: {driver.title}")