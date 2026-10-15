from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.name_input = page.get_by_test_id("ContactName")
        self.email_input = page.get_by_test_id("ContactEmail")
        self.phone_input = page.get_by_test_id("ContactPhone")
        self.subject_input = page.get_by_test_id("ContactSubject")
        self.message_input = page.get_by_test_id("ContactDescription")
        self.submit_button = page.get_by_role("button", name="Submit")

    def load(self):
        self.page.goto("/")

    def fill_contact_form(self, name, email, phone, subject, message):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.phone_input.fill(phone)
        self.subject_input.fill(subject)
        self.message_input.fill(message)

    def submit_contact_form(self):
        self.submit_button.click()

    def success_heading(self, name):
        return self.page.get_by_text(f"Thanks for getting in touch {name}!")