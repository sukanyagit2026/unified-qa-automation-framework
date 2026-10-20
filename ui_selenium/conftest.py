import os

import pytest
from selenium import webdriver

BASE_URL = "https://automationintesting.online"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    headless = os.getenv("HEADLESS") == "1"

    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        browser = webdriver.Chrome(options=options)
    else:
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        browser = webdriver.Firefox(options=options)

    browser.set_window_size(1366, 900)
    yield browser
    browser.quit()