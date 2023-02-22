from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.wait import WebDriverWait

import helper_tests

INET_SITE = "https://www.inet.se/"

class TestClass:


    # Setup and Teardown for the whole test class
    # scope defines which tests a single invocation of the fixture will apply for
    @pytest.fixture(scope="class")
    def load_driver(self):

        # Selenium 4.6 and above use a BETA version of Selenium Manager which automatically handles the browser drivers
        # If we have an older version, or if Selenium Managers somehow does not work on your system, follow this guide for installing the correct driver:
        # https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/

        driver = webdriver.Chrome()

        # NOT THE BEST SOLUTION BUT USE IT AS A PLACEHOLDER
        # WARNING: THIS DOES NOT WORK WITH EXPLICIT WAIT
        # driver.implicitly_wait(5)

        yield driver

        print('RUN CLASS TEARDOWN')

        driver.quit()


    # Setup and Teardown for every single test
    @pytest.fixture
    def get_inet_site(self, load_driver):

        driver = load_driver

        # Load iceberry website
        driver.get(INET_SITE)

        yield driver

        print('RUN TEST TEARDOWN')

        driver.delete_all_cookies()
        
    def test_1(self, get_inet_site):
        # Load Selenium webdriver
        driver = get_inet_site

        # Test that iceberry is part of the url
        helper_tests.boolean_assert("inet" in driver.current_url, f"Expected inet in url, got: {driver.current_url}")
    
    def test_advanced_2(self, get_inet_site):
        # Load Selenium webdriver
        driver = get_inet_site

        # Find products page link
        datorer_link = driver.find_element(By.XPATH, '//*[@id="react-root"]/div[3]/div/div/div[2]/div[2]/div[3]/div/a[1]/div')

        # Click on products page link
        datorer_link.click()

        # Including explicit wait
        # WARNING: This does not work together with implicit wait
        h1 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h1"))
        expected_h1 = "Datorer"

        #print('Scar Original'==scar_original.text)
        # Test that the text contains "Scar Original"
        helper_tests.boolean_assert(expected_h1 in h1.text, f"Expected {expected_h1} in text for h1, got: {h1.text}")

        expected_title = "Datorer - Köp online här"

        # Test that url now contains products
        helper_tests.boolean_assert(expected_title in driver.title, f"Expected {expected_title} in title, got: {driver.title}")