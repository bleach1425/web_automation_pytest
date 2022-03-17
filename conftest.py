from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
import json


def pytest_addoption(parser):
    parser.addoption("--email", action="store", help="input email")
    parser.addoption("--password", action="store", help="input password")

@pytest.fixture(scope="session")
def params(request):
    account, checkpoint = {}, {}

    # Args
    with open("account.json", mode='r') as f:
        account = json.load(f)
        email = account.get("email")
        password = account.get("password")

    # CheckPoint
    check_point3 = "https://rhinoshield.tw/pages/clear?bcolor=crystal_clear"
    check_point4 = "https://rhinoshield.tw/pages/clear?bcolor=crystal_clear&device=iphone-13"
    check_point6 = "iPhone 13 犀牛盾Clear透明手機殼 - 透明"

    # Save to dict
    account['email'] = email
    account['password'] = password
    checkpoint['check_point3'] = check_point3
    checkpoint['check_point4'] = check_point4
    checkpoint['check_point6'] = check_point6

    return account, checkpoint

@pytest.fixture(scope="class", params=["Chrome", "Edge"])
def driver_init(request):
    print("request: ", request)
    if request.param == "Chrome":
        print("Chrome")
        web_driver = webdriver.Chrome("./driver/chromedriver.exe")

    elif request.param == "Firefox":
        print("Firefox")
        web_driver = webdriver.Firefox("./driver/geckodriver.exe")
    
    elif request.param == "Safari":
        web_driver = webdriver.Safari("")
    
    elif request.param == "Edge":
        web_driver = webdriver.Edge("./driver/msedgedriver.exe")

    request.cls.driver = web_driver
    options = Options()
    options.add_argument("--disable-notifications")
    # settings
    web_driver.implicitly_wait(15)
    web_driver.maximize_window()
    web_driver.delete_all_cookies()
    yield
    
    
