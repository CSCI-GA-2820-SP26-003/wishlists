"""Step definitions for Wishlist UI behave tests (Selenium)."""

import requests
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

HTTP_200_OK = 200
HTTP_204_NO_CONTENT = 204
WAIT_TIMEOUT = 30


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


@given("no wishlists exist")
def step_no_wishlists_exist(context):
    """Delete all wishlists so each scenario starts from a clean state."""
    rest_endpoint = f"{context.base_url}/wishlists"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_200_OK

    for wishlist in context.resp.json():
        delete_resp = requests.delete(
            f"{rest_endpoint}/{wishlist['id']}",
            timeout=WAIT_TIMEOUT,
        )
        assert delete_resp.status_code == HTTP_204_NO_CONTENT
