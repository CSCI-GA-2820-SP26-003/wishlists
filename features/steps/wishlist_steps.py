"""Step definitions for Wishlist UI behave tests (Selenium)."""

import requests
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

HTTP_200_OK = 200
HTTP_204_NO_CONTENT = 204
HTTP_201_CREATED = 201
WAIT_TIMEOUT = 30
API_BASE_PATH = "/api/wishlists"


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
    rest_endpoint = f"{context.base_url}{API_BASE_PATH}"
    context.resp = requests.get(rest_endpoint, timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_200_OK

    for wishlist in context.resp.json():
        delete_resp = requests.delete(
            f"{rest_endpoint}/{wishlist['id']}",
            timeout=WAIT_TIMEOUT,
        )
        assert delete_resp.status_code == HTTP_204_NO_CONTENT


def create_wishlist_via_api(context, name, customer_id, description):
    payload = {
        "name": name,
        "customer_id": customer_id,
        "description": description,
    }
    create_resp = requests.post(
        f"{context.base_url}{API_BASE_PATH}",
        json=payload,
        timeout=WAIT_TIMEOUT,
    )
    assert create_resp.status_code == HTTP_201_CREATED
    return create_resp.json()


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


@when("I create a wishlist with valid details")
def step_create_wishlist_with_valid_details(context):
    """Create a wishlist using the browser UI and capture the created record."""
    context.driver.find_element(By.ID, "wishlist_name").clear()
    context.driver.find_element(By.ID, "wishlist_name").send_keys("Gaming Setup")
    context.driver.find_element(By.ID, "wishlist_customer_id").clear()
    context.driver.find_element(By.ID, "wishlist_customer_id").send_keys("12345")
    context.driver.find_element(By.ID, "wishlist_description").clear()
    context.driver.find_element(By.ID, "wishlist_description").send_keys(
        "PC and peripherals"
    )
    context.driver.find_element(By.ID, "create-btn").click()

    WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    context.created_wishlist = {
        "id": context.driver.find_element(By.ID, "wishlist_id").get_attribute("value"),
        "name": context.driver.find_element(By.ID, "wishlist_name").get_attribute("value"),
        "customer_id": context.driver.find_element(By.ID, "wishlist_customer_id").get_attribute(
            "value"
        ),
        "description": context.driver.find_element(
            By.ID, "wishlist_description"
        ).get_attribute("value"),
    }


@when('I press the "Create" button without entering a wishlist name')
def step_create_without_name(context):
    """Try creating from UI with missing name to trigger validation."""
    context.driver.find_element(By.ID, "wishlist_name").clear()
    context.driver.find_element(By.ID, "wishlist_customer_id").clear()
    context.driver.find_element(By.ID, "wishlist_customer_id").send_keys("12345")
    context.driver.find_element(By.ID, "wishlist_description").clear()
    context.driver.find_element(By.ID, "wishlist_description").send_keys(
        "PC and peripherals"
    )
    context.driver.find_element(By.ID, "create-btn").click()


@when("I retrieve the wishlist by ID")
def step_retrieve_wishlist_by_id(context):
    """Enter the wishlist id and click Retrieve in the UI."""
    wishlist_id = str(context.wishlist["id"])
    id_input = context.driver.find_element(By.ID, "wishlist_id")
    id_input.clear()
    id_input.send_keys(wishlist_id)
    context.driver.find_element(By.ID, "retrieve-btn").click()


@when("I retrieve that wishlist again")
def step_retrieve_wishlist_again(context):
    """Retrieve the current wishlist again by id."""
    step_retrieve_wishlist_by_id(context)


@when("I make the wishlist private from the web UI")
def step_make_wishlist_private_from_ui(context):
    """Click Make Private for the current wishlist id."""
    wishlist_id = str(context.wishlist["id"])
    id_input = context.driver.find_element(By.ID, "wishlist_id")
    id_input.clear()
    id_input.send_keys(wishlist_id)
    context.driver.find_element(By.ID, "make_private-btn").click()


@when("I enter a wishlist ID that does not exist")
def step_enter_missing_wishlist_id(context):
    """Enter a wishlist id that is not present in storage."""
    id_input = context.driver.find_element(By.ID, "wishlist_id")
    id_input.clear()
    id_input.send_keys("999999")


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


@then("I should see the newly created wishlist details")
def step_see_newly_created_wishlist_details(context):
    """Validate created wishlist is visible in form fields and results."""
    assert context.driver.find_element(By.ID, "wishlist_id").get_attribute(
        "value"
    ) != ""
    assert (
        context.driver.find_element(By.ID, "wishlist_name").get_attribute("value")
        == "Gaming Setup"
    )
    assert context.driver.find_element(By.ID, "wishlist_customer_id").get_attribute(
        "value"
    ) == "12345"
    assert (
        context.driver.find_element(By.ID, "wishlist_description").get_attribute("value")
        == "PC and peripherals"
    )
    table_text = context.driver.find_element(By.ID, "search_results").text
    assert "Gaming Setup" in table_text
    assert "12345" in table_text


@then("I should see the new wishlist in the results")
def step_see_new_wishlist_in_results(context):
    """Validate search results include the wishlist created in this scenario."""
    WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    table_text = context.driver.find_element(By.ID, "search_results").text
    assert context.created_wishlist["name"] in table_text
    assert context.created_wishlist["customer_id"] in table_text


@then("I should see an error message indicating the name is required")
def step_name_required_error(context):
    """Ensure UI validation message appears for missing name on create."""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element((By.ID, "flash_message"), "Name is required")
    )
    assert found


@then("the wishlist should show a private status")
def step_wishlist_shows_private_status(context):
    """Ensure the UI marks the wishlist as private."""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element_value((By.ID, "wishlist_is_private"), "true")
    )
    assert found
    table_text = context.driver.find_element(By.ID, "search_results").text
    assert "Private" in table_text


@then('I should see that "is_private" is true')
def step_is_private_true(context):
    """Assert private flag remains true after retrieval."""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element_value((By.ID, "wishlist_is_private"), "true")
    )
    assert found


@then("I should see an error message indicating the wishlist ID is required or invalid")
def step_wishlist_id_required_or_invalid(context):
    """Check UI validation for missing or invalid wishlist id."""
    WebDriverWait(context.driver, context.wait_seconds).until(
        lambda drv: drv.find_element(By.ID, "flash_message").text.strip() != ""
    )
    message = context.driver.find_element(By.ID, "flash_message").text
    assert (
        "Wishlist ID is required" in message
        or "Wishlist ID must be an integer" in message
    )


@then("I should see an error message indicating the wishlist was not found")
def step_wishlist_not_found_error(context):
    """Check UI error for missing wishlist id in backend."""
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element((By.ID, "flash_message"), "not found")
    )
    assert found


@when("I delete the wishlist by ID")
def step_delete_wishlist_by_id(context):
    """Enter the wishlist id and click Delete in the UI."""
    wishlist_id = str(context.wishlist["id"])
    id_input = context.driver.find_element(By.ID, "wishlist_id")
    id_input.clear()
    id_input.send_keys(wishlist_id)
    context.driver.find_element(By.ID, "delete-btn").click()


@then("I should not see the deleted wishlist in the results")
def step_deleted_wishlist_not_in_results(context):
    """Search by customer and confirm the deleted wishlist id is absent."""
    customer_input = context.driver.find_element(By.ID, "wishlist_customer_id")
    customer_input.clear()
    customer_input.send_keys(str(context.wishlist["customer_id"]))
    context.driver.execute_script(
        "document.getElementById('flash_message').textContent = '';"
    )
    context.driver.find_element(By.ID, "search-btn").click()

    found = WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    assert found
    rows = context.driver.find_elements(By.CSS_SELECTOR, "#results_body tr")
    returned_ids = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 1:
            returned_ids.append(cells[0].text.strip())

    assert str(context.wishlist["id"]) not in returned_ids


@given("multiple wishlists exist")
def step_multiple_wishlists_exist(context):
    step_no_wishlists_exist(context)
    first = create_wishlist_via_api(
        context,
        "Gaming Setup",
        12345,
        "PC and peripherals",
    )
    second = create_wishlist_via_api(
        context,
        "Travel Gear",
        67890,
        "Luggage and accessories",
    )
    context.wishlists = [first, second]


@when("I search for wishlists")
def step_search_for_wishlists(context):
    context.driver.find_element(By.ID, "search-btn").click()


@then("I should see all wishlists in the results")
def step_see_all_wishlists_in_results(context):
    expected_ids = {str(wishlist["id"]) for wishlist in context.wishlists}
    WebDriverWait(context.driver, context.wait_seconds).until(
        lambda drv: all(
            wishlist_id in drv.find_element(By.ID, "search_results").text
            for wishlist_id in expected_ids
        )
    )
    table_text = context.driver.find_element(By.ID, "search_results").text
    for wishlist_id in expected_ids:
        assert wishlist_id in table_text


@then("I should see more than one wishlist in the results")
def step_see_more_than_one_wishlist_in_results(context):
    WebDriverWait(context.driver, context.wait_seconds).until(
        lambda drv: len(drv.find_elements(By.CSS_SELECTOR, "#results_body tr")) > 1
    )
    rows = context.driver.find_elements(By.CSS_SELECTOR, "#results_body tr")
    assert len(rows) > 1


@then('I should not see "{text}" in the results')
def step_should_not_see_in_results(context, text):
    """Assert the results table does NOT contain the given text."""
    WebDriverWait(context.driver, context.wait_seconds).until(
        ec.text_to_be_present_in_element((By.ID, "flash_message"), "Success")
    )
    table_text = context.driver.find_element(By.ID, "search_results").text
    assert text not in table_text


@then('the wishlist name should be updated to "{name}"')
def step_wishlist_name_updated(context, name):
    """Verify the updated wishlist name is shown in the UI and persisted."""
    assert (
        context.driver.find_element(By.ID, "wishlist_name").get_attribute("value")
        == name
    )
    table_text = context.driver.find_element(By.ID, "search_results").text
    assert name in table_text

    response = requests.get(
        f"{context.base_url}{API_BASE_PATH}/{context.wishlist['id']}",
        timeout=WAIT_TIMEOUT,
    )
    assert response.status_code == HTTP_200_OK
    updated_wishlist = response.json()
    assert updated_wishlist["name"] == name
    context.wishlist["name"] = name


@then('the wishlist description should be updated to "{description}"')
def step_wishlist_description_updated(context, description):
    """Verify the updated wishlist description is shown in the UI and persisted."""
    assert (
        context.driver.find_element(By.ID, "wishlist_description").get_attribute(
            "value"
        )
        == description
    )
    table_text = context.driver.find_element(By.ID, "search_results").text
    assert description in table_text

    response = requests.get(
        f"{context.base_url}{API_BASE_PATH}/{context.wishlist['id']}",
        timeout=WAIT_TIMEOUT,
    )
    assert response.status_code == HTTP_200_OK
    updated_wishlist = response.json()
    assert updated_wishlist["description"] == description
    context.wishlist["description"] = description
