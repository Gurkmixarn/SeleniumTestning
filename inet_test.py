from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

import helper_tests as ht

INET_SITE = "https://www.inet.se/"

#datorer_xpath_side = '//*[@id="react-root"]/div[3]/div/div/div[2]/div[2]/div[3]/div/a[1]/div'
side_xpath_incomplete = '//span[normalize-space()="'
datorer_xpath_side = '//span[normalize-space()="Datorer"]'
number_in_cart = "#cart-button > div > svg > text"
cart_xpath = "/html/body/div[1]/div[2]/nav/div/div/div[4]"
search_xpath = "/html/body/div[1]/div[2]/header/div[2]/div/nav/div[2]/input"
product_types = ["Bildskärm","Datorer","Dator­komponenter","Datortillbehör","Extern Lagring","Hem/Fritid/Hälsa","Kablar/Adaptrar","Ljud/Bild","Mobiltelefon","Nätverk","Presentkort","Programvara","Skrivare/Scanner","Smarta Hem","Spel/Konsol/VR","Surfplatta"]



class TestClass:
    @pytest.fixture(scope="class")
    def load_driver(self):
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
        #driver = webdriver.Chrome()

        yield driver

        print('RUN CLASS TEARDOWN')
        driver.delete_all_cookies()

        driver.quit()

    @pytest.fixture
    def get_inet_site(self, load_driver):

        driver = load_driver
        driver.delete_all_cookies()

        driver.get(INET_SITE)

        #cookies_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/button[1]")
        #cookies_button.click()
        try:
            ht.click_by_xpath(driver,'//button[normalize-space()="Jag förstår"]')
        except:
            pass


        yield driver

        print('RUN TEST TEARDOWN')

        
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
        ht.click_by_xpath(driver,"/html/body/div[1]/div[3]/div/div/div[1]/div/div[2]/ol/li[3]/div[2]/div/ol/li[1]/div[2]/div/ol/li[1]/div[2]/div/ol/li/a")
        h1 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h1"))
        expected_h1 = "Chromebook - ASUS"
        ht.boolean_assert(expected_h1 in h1.text, f"Expected {expected_h1} in text for h1, got: {h1.text}")
        ht.boolean_assert("chromebook" in driver.current_url,f"Expected chromebook in url, got :{driver.current_url}")

    def test_4_add_to_cart(self,get_inet_site):
        driver = get_inet_site

        ht.click_by_xpath(driver,datorer_xpath_side)
        ht.click_by_xpath(driver,'//button[normalize-space()="Köp"]')
        current_items_in_cart = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, number_in_cart).text)
        ht.boolean_assert(current_items_in_cart == "1",f"Expected 1 item in cart, got:{current_items_in_cart}")

    def test_5_all_side_links_product_categories(self,get_inet_site):
        driver = get_inet_site
        for category in product_types:
            complete_xpath = side_xpath_incomplete + category + '"]'
            ht.click_by_xpath(driver,complete_xpath)
            h1 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h1").text)
            ht.boolean_assert(category == h1,f"Expected {category} in h1 got: {h1}")
            #Next line would work but datorskärm =! bildskärm..........
            #ht.boolean_assert(category in driver.title, f"Expected {category} in title, got: {driver.title}")
    def test_6_add_alot_to_cart(self,get_inet_site):
        driver = get_inet_site
        ht.click_by_xpath(driver,datorer_xpath_side)
        buttons = driver.find_elements(By.XPATH,'//button[normalize-space()="Köp"]')
        amount_in_cart = 0

        for button in buttons:
            button.click()
            amount_in_cart +=1
            ht.click_by_xpath(driver,"/html/body/div[1]/div[2]/nav/div/div/div[5]")

        current_items_in_cart = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, number_in_cart).text)
        ht.boolean_assert(len(buttons) == int(current_items_in_cart),f"Expected {len(buttons)} objects in cart, got:{current_items_in_cart}")
    def test_7_search_bar(self,get_inet_site):
        driver = get_inet_site

        driver.find_element(By.XPATH,search_xpath).send_keys("Datorer")
        ht.click_by_xpath(driver,"/html/body/div[1]/div[2]/header/div[2]/div/nav/div[2]/div[2]/div[1]/ul/li/a/mark")

        h1 = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.TAG_NAME, "h1"))
        expected_h1 = "Datorer"
        ht.boolean_assert(expected_h1 in h1.text, f"Expected {expected_h1} in text for h1, got: {h1.text}")

        expected_title = "Datorer - Köp online här"
        ht.boolean_assert(expected_title in driver.title, f"Expected {expected_title} in title, got: {driver.title}")
    def test_8_right_item_in_cart(self,get_inet_site):
        driver = get_inet_site

        ht.click_by_xpath(driver,datorer_xpath_side)
        product_name = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div[2]/div[2]/section/div[6]/div/div/div[1]/div[2]/a/h3").text
        product_price = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div[2]/div[2]/section/div[6]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div/span").text
        ht.click_by_xpath(driver,'//button[normalize-space()="Köp"]')
        WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "/html/body/div[1]/div[2]/nav/div/div/div[6]/div/div/div/div[1]/ul/li/div/article/div[1]/div[1]"))
        ht.click_by_xpath(driver,"/html/body/div[1]/div[2]/nav/div/div/div[6]/div/div/div/a")
        product_name_cart = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div[2]/div/div/div/ul/li/div/article/div[1]/div[1]/a")).text
        product_price_cart = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div[2]/div/div/div/ul/li/div/article/div[3]/span/span/span").text
        ht.boolean_assert(product_name == product_name_cart,f"Expected {product_name} and {product_name_cart} to match.")
        product_price_numbers = ht.remove_non_numbers(product_price)
        product_price_cart_numbers = ht.remove_non_numbers(product_price_cart)
        ht.boolean_assert(product_price_numbers == product_price_cart_numbers,f"Expected {product_price_numbers} and {product_price_cart_numbers} to match.")


        



        