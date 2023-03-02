from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.wait import WebDriverWait

def simple_assert(gotten_val, expected_val):
    assert gotten_val == expected_val, f"Assertion failed, expected: {expected_val}, got: {gotten_val}"


def boolean_assert(value, message):
    assert value, message
def remove_non_numbers(str1):
    try:
        return int(''.join(i for i in str1 if i.isdigit()))
    except:
        print("Error value in function!")
        return 0
def click_by_xpath(driver,xpath):
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.XPATH, xpath))
    driver.find_element(By.XPATH,xpath).click()
def click_by_css(driver,css):
    WebDriverWait(driver, timeout=5).until(lambda d: d.find_element(By.CSS_SELECTOR, css))
    driver.find_element(By.CSS_SELECTOR,css).click()