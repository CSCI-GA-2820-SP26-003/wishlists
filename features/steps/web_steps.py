"""Generic Selenium web steps for the Wishlist UI."""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

ID_PREFIX = "wishlist_"


@given('I am on the "Home Page"')
@when('I visit the "Home Page"')
def step_impl(context):
    """Load the browser UI."""
    context.driver.get(context.base_url)


@given('I set the "{element_name}" to "{text_string}"')
@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    """Fill in a text input or textarea."""
    normalized_name = element_name.lower().replace(" ", "_")
    element_id = ID_PREFIX + normalized_name
    if normalized_name.startswith("wishlist_"):
        element_id = normalized_name
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@given('I press the "{button}" button')
@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button by its label."""
    button_id = button.lower().replace(" ", "_") + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Check the flash area for a message."""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"),
            message,
        )
    )
    assert found


@then('I should see "{text}" in the results')
def step_impl(context, text):
    """Check the search results table for the expected text."""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "search_results"),
            text,
        )
    )
    assert found
