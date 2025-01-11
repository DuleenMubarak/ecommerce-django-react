import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TestEndToEnd():
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1550, 830)
  
    def teardown_method(self, method):
        self.driver.quit()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        # self.driver.close()
  
    def test_register(self):
        # self.driver.get("http://127.0.0.1:8000/")
        # self.driver.set_window_size(1550, 830)
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        self.driver.find_element(By.ID, "name").send_keys("tester")
        self.driver.find_element(By.ID, "email").send_keys("tester@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("tester123")
        self.driver.find_element(By.ID, "passwordConfirm").send_keys("tester123")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        assert self.driver.find_element(By.ID, "username").text == "TESTER"
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
    
  
    def test_signin(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(1550, 830)
        self.driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(2)").click()
        self.driver.find_element(By.ID, "email").send_keys("tester@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("tester123")
        self.driver.find_element(By.CSS_SELECTOR, ".mt-3").click()
        assert self.driver.find_element(By.ID, "username").text == "TESTER"
    
    def test_addproducttocart(self):
        self.driver.get("http://127.0.0.1:8000")
        self.driver.set_window_size(1550, 830)
        self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(1) strong").click()
        self.driver.execute_script("window.scrollTo(0,45.599998474121094)")
        self.driver.find_element(By.CSS_SELECTOR, ".w-100").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h1").text == "SHOPPING CART"
    
    
    def test_searchforproduct(self):
        self.driver.get("http://127.0.0.1:8000")
        self.driver.set_window_size(1550, 830)
        self.driver.find_element(By.NAME, "q").click()
        self.driver.find_element(By.NAME, "q").send_keys("rolling drum")
        self.driver.find_element(By.CSS_SELECTOR, ".p-2").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".my-3")
        assert len(elements) > 0
        assert self.driver.find_element(By.CSS_SELECTOR, "strong").text == "Rolling drum hand-eye coordination"
    
    def test_writeareview(self):
        self.driver.get("http://127.0.0.1:8000")
        self.driver.set_window_size(1550, 830)
        self.driver.find_element(By.CSS_SELECTOR, ".col-xl-3:nth-child(1) .card-img").click()
        self.driver.find_element(By.ID, "rating").click()
        dropdown = self.driver.find_element(By.ID, "rating")
        dropdown.find_element(By.XPATH, "//option[. = '4 - Very Good']").click()
        self.driver.find_element(By.ID, "comment").click()
        self.driver.find_element(By.ID, "comment").send_keys("testing review")
        self.driver.find_element(By.CSS_SELECTOR, ".my-3:nth-child(3)").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".list-group:nth-child(2) > .list-group-item:nth-child(1)")
        assert len(elements) > 0
        assert self.driver.find_element(By.XPATH, "//strong[contains(.,\'tester\')]").text == "tester"
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".fade")
        assert len(elements) == 0
    
