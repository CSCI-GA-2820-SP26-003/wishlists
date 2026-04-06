"""Step definitions for Wishlist UI behave tests."""

import os
import requests
from behave import given

HTTP_200_OK = 200
HTTP_204_NO_CONTENT = 204
WAIT_TIMEOUT = 30


@given("the Wishlist service is running")
def step_impl(context):
    """Confirm the service is reachable."""
    context.base_url = os.getenv("BASE_URL", "http://localhost:8080")
    context.resp = requests.get(context.base_url + "/", timeout=WAIT_TIMEOUT)
    assert context.resp.status_code == HTTP_200_OK


@given("no wishlists exist")
def step_impl(context):
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
