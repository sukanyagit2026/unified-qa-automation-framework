import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://automationintesting.online/")
    page.get_by_role("link", name="Book now").nth(1).click()
    page.get_by_role("img", name="Room Image").click(modifiers=["Alt"])
    page.locator("div:nth-child(3) > .rbc-row-bg > div:nth-child(5)").click()
    page.get_by_role("button", name="Reserve Now").click()
    page.get_by_role("textbox", name="Firstname").click()
    page.get_by_role("textbox", name="Firstname").fill("sukanya")
    page.get_by_role("textbox", name="Lastname").click()
    page.get_by_role("textbox", name="Lastname").fill("boopathirajan")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill("bala@gmail.com")
    page.get_by_role("textbox", name="Phone").click()
    page.get_by_role("textbox", name="Phone").fill("89045678")
    page.get_by_role("button", name="Reserve Now").click()
    page.get_by_role("textbox", name="Phone").click()
    page.get_by_role("textbox", name="Phone").fill("89045678678")
    page.get_by_role("button", name="Reserve Now").click()
