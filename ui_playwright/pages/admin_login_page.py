from playwright.sync_api import Page


class AdminLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_role("textbox", name="Username")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.logout_button = page.get_by_role("button", name="Logout")
        self.error_message = page.get_by_text("Invalid credentials")

    def load(self):
        self.page.goto("/admin", wait_until="domcontentloaded")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def logout(self):
        self.logout_button.click()