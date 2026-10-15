import random
from datetime import date, timedelta

from playwright.sync_api import expect

from ui_playwright.pages.booking_page import BookingPage

ROOM_ID = 1


def random_stay(nights=2):
    start = date.today() + timedelta(days=random.randint(60, 700))
    end = start + timedelta(days=nights)
    return start.isoformat(), end.isoformat()


def test_book_room_success(page):
    checkin, checkout = random_stay()
    booking = BookingPage(page)

    booking.load(ROOM_ID, checkin, checkout)
    booking.open_booking_form()
    booking.fill_guest_details(
        "Sukanya", "Boopathirajan", "sukanya.test@example.com", "89045678678"
    )
    booking.submit()

    expect(booking.confirmation_heading).to_be_visible()
    expect(booking.confirmed_dates(checkin, checkout)).to_be_visible()