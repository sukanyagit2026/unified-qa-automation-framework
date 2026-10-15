from playwright.sync_api import expect


def test_contact_form_success(home_page):
    home_page.fill_contact_form(
        name="Sukanya",
        email="sukanya@example.com",
        phone="80863456782",
        subject="Room booking",
        message="I would like to book a room for next weekend.",
    )
    home_page.submit_contact_form()

    expect(home_page.success_heading("Sukanya")).to_be_visible()