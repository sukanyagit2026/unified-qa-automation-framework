from playwright.sync_api import Page


class BookingPage:
    def __init__(self, page: Page):
        self.page = page
        self.reserve_button = page.get_by_role("button", name="Reserve Now")
        self.firstname_input = page.get_by_role("textbox", name="Firstname")
        self.lastname_input = page.get_by_role("textbox", name="Lastname")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.phone_input = page.get_by_role("textbox", name="Phone")
        self.confirmation_heading = page.get_by_text("Booking Confirmed", exact=True)

    def load(self, room_id, checkin, checkout):
        self.page.goto(
            f"/reservation/{room_id}?checkin={checkin}&checkout={checkout}",
            wait_until="domcontentloaded",
        )

    def open_booking_form(self):
        self.reserve_button.click()

    def fill_guest_details(self, firstname, lastname, email, phone):
        self.firstname_input.fill(firstname)
        self.lastname_input.fill(lastname)
        self.email_input.fill(email)
        self.phone_input.fill(phone)

    def submit(self):
        self.reserve_button.click()

    def confirmed_dates(self, checkin, checkout):
        return self.page.get_by_text(f"{checkin} - {checkout}", exact=True)

    def error_message(self, text):
        return self.page.get_by_text(text, exact=True)