import pytest

from ui_playwright.pages.admin_login_page import AdminLoginPage
from ui_playwright.pages.home_page import HomePage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": "https://automationintesting.online",
    }


@pytest.fixture
def home_page(page):
    home = HomePage(page)
    home.load()
    return home


@pytest.fixture
def admin_login_page(page):
    admin = AdminLoginPage(page)
    admin.load()
    return admin