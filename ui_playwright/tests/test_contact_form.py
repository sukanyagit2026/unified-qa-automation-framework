import pytest
from playwright.sync_api import expect

VALID_DATA = {
    "name": "Sukanya",
    "email": "sukanya@example.com",
    "phone": "80863456782",
    "subject": "Room booking",
    "message": "I would like to book a room for next weekend.",
}


def submit_form(home_page, **overrides):
    data = {**VALID_DATA, **overrides}
    home_page.fill_contact_form(**data)
    home_page.submit_contact_form()
    return data


def test_contact_form_success(home_page):
    data = submit_form(home_page)
    expect(home_page.success_heading(data["name"])).to_be_visible()


def test_empty_form_shows_required_errors(home_page):
    home_page.submit_contact_form()

    for message in [
        "Name may not be blank",
        "Email may not be blank",
        "Phone may not be blank",
        "Subject may not be blank",
        "Message may not be blank",
    ]:
        expect(home_page.error_message(message)).to_be_visible()


@pytest.mark.parametrize(
    "field, bad_value, expected_error",
    [
        ("name", "", "Name may not be blank"),
        ("email", "", "Email may not be blank"),
        ("phone", "8086345678", "Phone must be between 11 and 21 characters."),
        ("subject", "Hi", "Subject must be between 5 and 100 characters."),
        ("message", "Hello", "Message must be between 20 and 2000 characters."),
    ],
    ids=[
        "blank-name",
        "blank-email",
        "phone-too-short",
        "subject-too-short",
        "message-too-short",
    ],
)
def test_contact_form_validation_errors(home_page, field, bad_value, expected_error):
    data = submit_form(home_page, **{field: bad_value})

    expect(home_page.error_message(expected_error)).to_be_visible()
    expect(home_page.success_heading(data["name"])).not_to_be_visible()


@pytest.mark.parametrize(
    "field, boundary_value",
    [
        ("phone", "1" * 11),
        ("subject", "a" * 5),
        ("message", "b" * 20),
    ],
    ids=["phone-min-11", "subject-min-5", "message-min-20"],
)
def test_contact_form_minimum_length_accepted(home_page, field, boundary_value):
    data = submit_form(home_page, **{field: boundary_value})
    expect(home_page.success_heading(data["name"])).to_be_visible()