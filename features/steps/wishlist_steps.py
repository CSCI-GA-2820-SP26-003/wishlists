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


@given("a wishlist exists")
def step_wishlist_exists(context):
    """Create one wishlist through the UI for retrieval tests."""
    context.driver.get(context.base_url)
    context.driver.find_element(By.ID, "wishlist_name").send_keys("Gaming Setup")
    context.driver.find_element(By.ID, "wishlist_customer_id").send_keys("12345")
    context.driver.find_element(By.ID, "wishlist_description").send_keys(
        "PC and peripherals"
    )
    context.driver.find_element(By.ID, "create-btn").click()

    found = WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    assert found

    context.wishlist = {
        "id": int(
            context.driver.find_element(By.ID, "wishlist_id").get_attribute("value")
        ),
        "name": "Gaming Setup",
        "customer_id": 12345,
        "description": "PC and peripherals",
    }


@when("I retrieve the wishlist by ID")
def step_retrieve_wishlist_by_id(context):
    """Enter the wishlist id and click Retrieve in the UI."""
    wishlist_id = str(context.wishlist["id"])
    id_input = context.driver.find_element(By.ID, "wishlist_id")
    id_input.clear()
    id_input.send_keys(wishlist_id)
    context.driver.find_element(By.ID, "retrieve-btn").click()


@then("I should see the wishlist details")
def step_see_wishlist_details(context):
    """Ensure retrieval succeeded and details are shown in UI."""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    assert found
    table_text = context.driver.find_element(By.ID, "search_results").text
    assert str(context.wishlist["id"]) in table_text


@then("I should see the correct wishlist information")
def step_see_correct_wishlist_information(context):
    """Validate key fields shown on the page match the created wishlist."""
    assert context.driver.find_element(By.ID, "wishlist_id").get_attribute(
        "value"
    ) == str(context.wishlist["id"])
    assert (
        context.driver.find_element(By.ID, "wishlist_name").get_attribute("value")
        == context.wishlist["name"]
    )
    assert context.driver.find_element(By.ID, "wishlist_customer_id").get_attribute(
        "value"
    ) == str(context.wishlist["customer_id"])
