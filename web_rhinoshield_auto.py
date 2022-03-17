from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import pyautogui

def choice_option(item, img):
    dropdown_select = Select(self.browser.find_element_by_xpath('//*[@id="shipping"]/select')).select_by_visible_text(item)
    assert pyautogui.locateOnScreen(img, confidence=0.95) != None, "Select family not work"
    time.sleep(1)


class TestCase:
    def __init__(self):
        # Setting
        self.browser = webdriver.Chrome("./chromedriver.exe")
        options = Options()
        options.add_argument("--disable-notifications")
        self.browser.implicitly_wait(15)
        self.browser.maximize_window()
        self.browser.delete_all_cookies()
        
        # Check
        self.check_point3 = "https://rhinoshield.tw/pages/clear?bcolor=crystal_clear"
        self.check_point4 = "https://rhinoshield.tw/pages/clear?bcolor=crystal_clear&device=iphone-13"
        self.check_point6 = "iPhone 13 犀牛盾Clear透明手機殼 - 透明"
    
    def test_go_page(self):
        """
        1. Go Website
        """
        self.browser.get("https://rhinoshield.tw/")
    
    def test_click_nav_bar(self):
        """
        1. Clear product button
        2. Click Type Clear
        3. Checkpoint3
        """
        # Step1
        product_button = self.browser.find_element_by_xpath('//*[@id="navigation-bar"]/div[2]/div/div[1]/div[3]/dl/dd[2]')
        assert product_button != None, "Can't Find product bottom"
        product_button.click()
        
        # Step2
        checkurl = self.browser.current_url
        TypeClear = self.browser.find_element_by_xpath('//*[@id="product-drop-down"]/ul/li[1]/a/img')
        assert TypeClear != None, "Can't Find type Clear"
        TypeClear.click()
        
        # Step3
        while checkurl == self.browser.current_url:
            pass
        
        time.sleep(1)
        assert self.check_point3 == self.browser.current_url, "Checkpoint3 Url Error"
    
    def test_choice_cellphone_type(self):
        """
        1. Control dropdown menu and choice iPhone 13
        2. Checkpoint4
        """
        
        # Step1
        dropdown_select = Select(self.browser.find_element_by_xpath('//*[@id="device-selector"]/select')).select_by_visible_text("iPhone 13")
        
        # Step2
        time.sleep(3) # wait url redirect
        assert self.check_point4 == self.browser.current_url, "Checkpoint4 Url Error"
        
    def test_carts(self):
        """
        1. Click add carts button
        2. Close recommend
        3. Click carts button
        4. Check carts have product
        5. Checkpoint6
        """
        # Step1
        addcarts = self.browser.find_element_by_xpath('//*[@id="clear-page"]/div/div[2]/div/section[2]/section[4]/div[3]/button')
        assert addcarts != None, "Can't find add carts button"
        addcarts.click()
        
        # Step2
        addcarts = self.browser.find_element_by_xpath('//*[@id="add__on"]/div[3]/button')
        assert addcarts != None, "Can't close recommend"
        addcarts.click()
        
        # Step3
        cartsbotton = self.browser.find_element_by_xpath('//*[@id="navigation-bar"]/div[2]/div/div[2]/div/div[1]/div[1]/div/a/p')
        assert cartsbotton != None, "Can't Click carts button"
        cartsbotton.click()
        
        # Step4
        product = self.browser.find_element_by_xpath('//*[@id="CartProducts"]/div/div[2]/a/div')
        assert cartsbotton != None, "Carts don't have any product"
        
        # Step5
        product_title = self.browser.find_element_by_xpath('//*[@id="CartProducts"]/div/div[2]/a/div').text
        assert product_title == self.check_point6, "Add product error"
        print("All Test End.")
        
        # 3 second check result and close
        time.sleep(3)
        self.browser.close()
    
    def test_checkout(self):
        """
        1. 取貨方式組合確認
        """
        pickup_list = ["全家超商取貨", "7-11 超商取貨", "黑貓寄送", "海外寄送"]
        pickup_img = ["family.png", '7-11.png', 'blackcat.png', 'outsea.png']
        pay_list = ["信用卡付款", "取貨付款"]
        pay_img

        # pick up check
        [choice_option(pickup_list[n], pickup_img[n]) for n in range(len(pickup_list))]
        
        # pay check
        [choice_option(pay_list[n], pay_img[n]) for n in range(pay_list)]
        
    def main(self):
        # runtime
        runtime = 1
        
        # work
        for n in range(runtime):
            self.test_go_page()
            self.test_click_nav_bar()
            self.test_choice_cellphone_type()
            self.test_carts()
        

if __name__ == "__main__":
    func = TestCase()
    func.main()
    