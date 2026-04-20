import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scenarios("welcome.feature")

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--no-sandbox")
    #options.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=options)
    d.set_window_size(1280, 800)
    yield d
    d.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, timeout=5)


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_input(driver, label_text):
    """Return an input element by its associated label text."""
    label_map = {
        "Full name": "field1",
        "Email address": "field2",
    }
    return driver.find_element(By.ID, label_map[label_text])


def is_page_active(driver, page_id):
    page = driver.find_element(By.ID, page_id)
    return "active" in page.get_attribute("class")


# ── Given ─────────────────────────────────────────────────────────────────────

@given("the user is on the Welcome page")
def open_welcome_page(driver):
    driver.get("file:///Users/guruppatra/Downloads/app.html")  # update path as needed
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "form-page"))
    )


# ── When ──────────────────────────────────────────────────────────────────────

@when(parsers.parse('the user enters "{value}" in the "{field}" field'))
def enter_text(driver, value, field):
    input_el = get_input(driver, field)
    input_el.clear()
    input_el.send_keys(value)


@when(parsers.parse('the user clicks the "{button}" button'))
def click_button(driver, button):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    target = next(
        (b for b in buttons if b.text.strip().lower() == button.lower()),
        None,
    )
    assert target is not None, f'Button "{button}" not found on the page'
    target.click()


# ── Then ──────────────────────────────────────────────────────────────────────

@then(parsers.parse('the page title should be "{expected}"'))
def check_page_title(driver, expected):
    title = driver.find_element(By.CLASS_NAME, "form-title")
    assert title.text.strip() == expected, (
        f'Expected title "{expected}", got "{title.text.strip()}"'
    )


@then(parsers.parse('the subtitle should be "{expected}"'))
def check_subtitle(driver, expected):
    subtitle = driver.find_element(By.CLASS_NAME, "form-subtitle")
    assert subtitle.text.strip() == expected, (
        f'Expected subtitle "{expected}", got "{subtitle.text.strip()}"'
    )


@then(parsers.parse('the "{label}" input field is visible'))
def check_input_visible(driver, label):
    input_el = get_input(driver, label)
    assert input_el.is_displayed(), f'Input "{label}" is not visible'


@then(parsers.parse('the "{button}" button is visible'))
def check_button_visible(driver, button):
    buttons = driver.find_elements(By.TAG_NAME, "button")
    target = next(
        (b for b in buttons if b.text.strip().lower() == button.lower()),
        None,
    )
    assert target is not None and target.is_displayed(), (
        f'Button "{button}" is not visible'
    )


@then("the user should be on the Dashboard page")
def check_on_dashboard(driver, wait):
    wait.until(lambda d: is_page_active(d, "dash-page"))
    assert is_page_active(driver, "dash-page"), "Dashboard page is not active"
    assert not is_page_active(driver, "form-page"), "Form page is still active"


@then("the user should remain on the Welcome page")
def check_on_welcome(driver):
    assert is_page_active(driver, "form-page"), "Welcome page is not active"
    assert not is_page_active(driver, "dash-page"), "Dashboard page is unexpectedly active"


@then(parsers.parse('the welcome message should be "{expected}"'))
def check_welcome_message(driver, expected):
    msg = driver.find_element(By.ID, "welcome-msg")
    assert msg.text.strip() == expected, (
        f'Expected welcome message "{expected}", got "{msg.text.strip()}"'
    )


@then(parsers.parse('the "{field}" field should be empty'))
def check_field_empty(driver, field):
    input_el = get_input(driver, field)
    assert input_el.get_attribute("value") == "", (
        f'Expected "{field}" to be empty, but it contains "{input_el.get_attribute("value")}"'
    )