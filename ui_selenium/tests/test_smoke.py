from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 20


def wait_for(driver, condition):
    return WebDriverWait(driver, TIMEOUT).until(condition)


def test_home_page_title(driver, base_url):
    driver.get(base_url)

    wait_for(driver, EC.title_is("Restful-booker-platform demo"))


def test_contact_form_success(driver, base_url):
    driver.get(base_url)

    wait_for(
        driver, EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='ContactName']"))
    ).send_keys("Sukanya")
    driver.find_element(By.CSS_SELECTOR, "[data-testid='ContactEmail']").send_keys(
        "sukanya.test@example.com"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-testid='ContactPhone']").send_keys(
        "89045678678"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-testid='ContactSubject']").send_keys(
        "Selenium smoke test"
    )
    driver.find_element(By.CSS_SELECTOR, "[data-testid='ContactDescription']").send_keys(
        "This is a Selenium smoke test message."
    )
    submit = driver.find_element(By.XPATH, "//button[text()='Submit']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit)
    wait_for(driver, EC.element_to_be_clickable(submit)).click()

    wait_for(
        driver,
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Thanks for getting in touch')]")
        ),
    )


def test_admin_login_success(driver, base_url):
    driver.get(base_url + "/admin")

    wait_for(driver, EC.visibility_of_element_located((By.ID, "username"))).send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("password")
    driver.find_element(By.ID, "doLogin").click()

    wait_for(driver, EC.url_contains("/admin/rooms"))