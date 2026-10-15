import re

import pytest
from playwright.sync_api import expect

ADMIN_USER = "admin"
ADMIN_PASSWORD = "password"


def test_admin_login_success(admin_login_page):
    admin_login_page.login(ADMIN_USER, ADMIN_PASSWORD)

    expect(admin_login_page.login_button).not_to_be_visible()
    expect(admin_login_page.error_message).not_to_be_visible()


def test_admin_logout_ends_session(admin_login_page):
    admin_login_page.login(ADMIN_USER, ADMIN_PASSWORD)
    expect(admin_login_page.login_button).not_to_be_visible()

    admin_login_page.logout()
    expect(admin_login_page.page).to_have_url(re.compile(r"/$"))

    admin_login_page.load()
    expect(admin_login_page.login_button).to_be_visible()


@pytest.mark.parametrize(
    "username, password",
    [
        (ADMIN_USER, "wrongpassword"),
        ("wronguser", ADMIN_PASSWORD),
        ("", ""),
    ],
    ids=["wrong-password", "wrong-username", "blank-credentials"],
)
def test_admin_login_invalid_credentials(admin_login_page, username, password):
    admin_login_page.login(username, password)

    expect(admin_login_page.error_message).to_be_visible()
    expect(admin_login_page.login_button).to_be_visible()