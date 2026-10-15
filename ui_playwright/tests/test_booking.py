import random
from datetime import date, timedelta

import pytest
from playwright.sync_api import expect

from ui_playwright.pages.booking_page import BookingPage

ROOM_ID = 1

VALID_GUEST = {
    "firstname": "Sukanya",
    "lastname": "Boopathirajan",
    "email": "sukanya.test@example.com",
    "phone": "89045678678",
}

EMPTY_FORM_ERRORS = {
    "Firstname should not be blank": 1,
    "Lastname should not be blank": 1,
    "size must be between 3 and 18": 1,
    "size must be between 3 and 30": 1,
    "size must be between 11 and 21": 1,
    "must not be empty": 2,
}


def random_stay(nights=2):
    start = date.today() + timedelta(days=random.randint(60, 700))
    end = start + timedelta(days=nights)
    return start.isoformat(), end.isoformat()


def open_booking_form(page):
    checkin, checkout = random_stay()
    booking = BookingPage(page)
    booking.load(ROOM_ID, checkin, checkout)
    booking.open_booking_form()
    return booking


def test_book_room_success(page):
    checkin, checkout = random_stay()
    booking = BookingPage(page)

    booking.load(ROOM_ID, checkin, checkout)
    booking.open_booking_form()
    booking.fill_guest_details(**VALID_GUEST)
    booking.submit()

    expect(booking.confirmation_heading).to_be_visible()
    expect(booking.confirmed_dates(checkin, checkout)).to_be_visible()


def test_booking_empty_form_shows_required_errors(page):
    booking = open_booking_form(page)
    booking.submit()

    for text, count in EMPTY_FORM_ERRORS.items():
        expect(booking.error_message(text)).to_have_count(count)
    expect(booking.confirmation_heading).not_to_be_visible()


@pytest.mark.parametrize(
    "overrides, expected_error",
    [
        ({"phone": "8" * 10}, "size must be between 11 and 21"),
        ({"phone": "8" * 22}, "size must be between 11 and 21"),
        ({"firstname": "Su"}, "size must be between 3 and 18"),
        ({"firstname": "S" * 19}, "size must be between 3 and 18"),
        ({"lastname": "Bo"}, "size must be between 3 and 30"),
        ({"lastname": "B" * 31}, "size must be between 3 and 30"),
    ],
    ids=[
        "phone-10-too-short",
        "phone-22-too-long",
        "firstname-2-too-short",
        "firstname-19-too-long",
        "lastname-2-too-short",
        "lastname-31-too-long",
    ],
)
def test_booking_field_length_errors(page, overrides, expected_error):
    booking = open_booking_form(page)
    booking.fill_guest_details(**{**VALID_GUEST, **overrides})