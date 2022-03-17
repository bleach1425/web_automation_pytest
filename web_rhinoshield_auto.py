from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import json
import pytest
import pyautogui


"""
犀牛盾自動化測試
"""


def choice_option(driver, item):
    """
    Option sent type test
    """
    pay_list = ["信用卡付款", "取貨付款"]
    if item == "全家超商取貨" or item == "7-11 超商取貨":
        dropdown_select = Select(driver.find_element_by_xpath('//*[@id="shipping"]/select')).select_by_visible_text(item)
        time.sleep(1)
        check = driver.find_element_by_class_name("rh-select__select")
        assert check, "Sent Type error"

        for pay in pay_list:
            Select(driver.find_element_by_xpath('//*[@id="payment"]/select')).select_by_visible_text(pay)
            time.sleep(1)

    elif item == "黑貓寄送":
        dropdown_select = Select(driver.find_element_by_xpath('//*[@id="shipping"]/select')).select_by_visible_text(item)
        time.sleep(1)
        assert driver.find_element_by_class_name('invoice-section__selector-note').text == "不支援郵政信箱", "Sent Type error"
    elif item == "海外寄送":
        url = "https://support.rhinoshield.io/hc/zh-tw/articles/360042082873--%E6%B5%B7%E5%A4%96%E5%8C%85%E8%A3%B9%E6%98%AF%E5%90%A6%E6%9C%83%E9%85%8C%E6%94%B6%E9%A1%8D%E5%A4%96%E8%B2%BB%E7%94%A8-ex-%E9%97%9C%E7%A8%85"
        dropdown_select = Select(driver.find_element_by_xpath('//*[@id="shipping"]/select')).select_by_visible_text(item)
        assert driver.find_element_by_class_name('invoice-section__selector-note').text == "海外購物須知 (請務必閱讀)。詳情", "Select payment error"
        
        check_url = driver.find_element_by_xpath('//*[@id="checkout-note-and-confirm"]/div/div[1]/div[1]/section[1]/div/div/p/a').get_attribute("href")
        assert url == check_url, "Outsea information error"


@pytest.mark.usefixtures("driver_init")
class BasicTest:
    pass

class TestCase(BasicTest):
    def test_settings(self, params):
        global param, xpath, id
        param = params
        xpath = lambda x: self.driver.find_element_by_xpath(x)
        id = lambda x: self.driver.find_element_by_id(x)

    def test_login(self):
        print("Login")
        """
        1. Go url
        2. Login
        """
        # Step1
        self.driver.get("https://rhinoshield.tw/")
        pyautogui.moveTo(1150, 117)

        # Step 2
        Login_button = xpath('//*[@id="navigation-bar"]/div[2]/div/div[2]/div/div[2]')
        assert Login_button, "Don't Find Login button"
        Login_button.click()
        time.sleep(2)
        id("customer_email").send_keys(param[0]["email"])
        time.sleep(1)
        id("customer_password").send_keys(param[0]["password"])
        xpath('//*[@id="customer_login"]/div/input').click()
        
    def test_click_nav_bar(self):
        """
        1. Clear product button
        2. Click Type Clear
        3. Checkpoint3
        """
        # Step1
        product_button = xpath('//*[@id="navigation-bar"]/div[2]/div/div[1]/div[3]/dl/dd[2]')
        assert product_button != None, "Can't Find product bottom"
        product_button.click()
        
        # Step2
        checkurl = self.driver.current_url
        TypeClear = xpath('//*[@id="product-drop-down"]/ul/li[1]/a/img')
        assert TypeClear != None, "Can't Find type Clear"
        TypeClear.click()
        
        # Step3
        while checkurl == self.driver.current_url:
            pass
        
        time.sleep(1)
        assert param[1]["check_point3"] == self.driver.current_url, "Checkpoint3 Url Error"
        print("Checkpoint3: ", param[1]["check_point3"] == self.driver.current_url)
    
    def test_choice_cellphone_type(self):
        """
        1. Control dropdown menu and choice iPhone 13
        2. Checkpoint4
        """
        
        # Step1
        dropdown_select = Select(xpath('//*[@id="device-selector"]/select')).select_by_visible_text("iPhone 13")
        
        # Step2
        time.sleep(3) # wait url redirect
        assert param[1]["check_point4"] == self.driver.current_url, "Checkpoint4 Url Error"
        print("Checkpoint4: ", param[1]["check_point4"] == self.driver.current_url)
        
    def test_carts(self):
        """
        1. Click add carts button
        2. Close recommend
        3. Click carts button
        4. Check carts have product
        5. Checkpoint6
        """
        # Step1
        addcarts = xpath('//*[@id="clear-page"]/div/div[2]/div/section[2]/section[4]/div[3]/button')
        assert addcarts != None, "Can't find add carts button"
        addcarts.click()
        
        # Step2
        addcarts = xpath('//*[@id="add__on"]/div[3]/button')
        assert addcarts != None, "Can't close recommend"
        addcarts.click()
        
        # Step3
        cartsbutton = xpath('//*[@id="navigation-bar"]/div[2]/div/div[2]/div/div[1]/div[1]/div/a/p')
        assert cartsbutton != None, "Can't Click carts button"
        cartsbutton.click()
        
        # Step4
        product = xpath('//*[@id="CartProducts"]/div/div[2]/a/div')
        assert cartsbutton != None, "Carts don't have any product"
        
        # Step5
        product_title = xpath('//*[@id="CartProducts"]/div/div[2]/a/div').text
        print("購物車商品名稱: ", product_title)
        assert product_title == param[1]["check_point6"], "Add product error"
        print("Checkpoint 6: ", product_title == param[1]["check_point6"])
        
        # 3 second check result and close
        time.sleep(3)
        print("All Test End.")
        self.driver.close()  

if __name__ == "__main__":
    pytest.main(["-v", "web_rhinoshield_auto.py"])
    