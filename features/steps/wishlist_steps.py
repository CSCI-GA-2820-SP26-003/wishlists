"""Step definitions for Wishlist UI behave tests (Selenium)."""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


@given("the Wishlist service is running")
def step_wishlist_service_running(context):
    """Load the app root; fails if nothing is listening (e.g. honcho not started)."""
    context.driver.get(context.base_url)
    WebDriverWait(context.driver, context.wait_seconds).until(
        ec.presence_of_element_located((By.TAG_NAME, "body"))
    )


@when("I visit the home page")
def step_visit_home_page(context):
    """Navigate to the home page."""
    context.driver.get(context.base_url)


@then('I should see "{text}"')
def step_should_see_text(context, text):
    """Assert visible page content includes the given substring."""
    WebDriverWait(context.driver, context.wait_seconds).until(
        lambda drv: text in drv.page_source
    )
