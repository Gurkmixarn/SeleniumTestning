from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.wait import WebDriverWait

import helper_tests as ht

INET_SITE = "https://www.inet.se/"

#datorer_xpath_side = '//*[@id="react-root"]/div[3]/div/div/div[2]/div[2]/div[3]/div/a[1]/div'
datorer_xpath_side = '//span[normalize-space()="Datorer"]'
number_in_cart = "#cart-button > div > svg > text"


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
        driver.delete_all_cookies()

        driver.get(INET_SITE)
        driver.maximize_window()

        #cookies_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/button[1]")
        #cookies_button.click()
        try:
            ht.click_by_xpath(driver,'//button[normalize-space()="Jag förstår"]')
        except:
            pass


        yield driver

        print('RUN TEST TEARDOWN')

        driver.delete_all_cookies()
        
    def test_1_assert_url_homepage(self, get_inet_site):
        driver = get_inet_site

        ht.boolean_assert("https://www.inet.se/" in driver.current_url, f"Expected inet in url, got: {driver.current_url}")
        ht.boolean_assert("För tekniken vi älskar - Inet.se" in driver.title,f"Expected Inet.se in title got:{driver.title}")
    
    def test_2_datorer_tab(self, get_inet_site):
        driver = get_inet_site

        ht.click_by_xpath(driver,datorer_xpath_side)

        h1 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h1"))
        expected_h1 = "Datorer"
        ht.boolean_assert(expected_h1 in h1.text, f"Expected {expected_h1} in text for h1, got: {h1.text}")

        expected_title = "Datorer - Köp online här"
        ht.boolean_assert(expected_title in driver.title, f"Expected {expected_title} in title, got: {driver.title}")

    def test_3_datorer_under_tabs(self,get_inet_site):
        driver = get_inet_site

        ht.click_by_css(driver,"[aria-label='expandera kategorin Datorer']")
        ht.click_by_css(driver,"[aria-label='expandera kategorin Bärbar dator']")
        ht.click_by_css(driver,"[aria-label='expandera kategorin Chromebook']")
        ht.click_by_css(driver,"[aria-label='expandera kategorin Chromebook']")
        ht.click_by_xpath(driver,"/html/body/div[1]/div[3]/div/div/div[1]/div/div[2]/ol/li[3]/div[2]/div/ol/li[1]/div[2]/div/ol/li[1]/div[2]/div/ol/li/a")
        h1 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h1"))
        expected_h1 = "Chromebook - ASUS"
        ht.boolean_assert(expected_h1 in h1.text, f"Expected {expected_h1} in text for h1, got: {h1.text}")
        ht.boolean_assert("chromebook" in driver.current_url,f"Expected chromebook in url, got :{driver.current_url}")

    def test_4_add_to_cart(self,get_inet_site):
        driver = get_inet_site

        ht.click_by_xpath(driver,datorer_xpath_side)
        #Breaks here for some reason sometimes?
        ht.click_by_xpath(driver,'//button[normalize-space()="Köp"]')
        current_items_in_cart = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, number_in_cart).text)
        ht.boolean_assert(current_items_in_cart == "1",f"Expected 1 item in cart, got:{current_items_in_cart}")

        