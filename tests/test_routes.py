######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
TestWishlist API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Wishlist, Item
from tests.factories import WishlistFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/wishlists"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Item).delete()  # clean up child records first
        db.session.query(Wishlist).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_get_wishlist(self):
        """It should Get a single Wishlist"""
        test_wishlist = WishlistFactory()
        test_wishlist.create()
        response = self.client.get(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_wishlist.name)
        self.assertEqual(data["customer_id"], test_wishlist.customer_id)

    def test_get_wishlist_not_found(self):
        """It should not Get a Wishlist that's not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("was not found", data["message"])

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_create_wishlist(self):
        """It should Create a new Wishlist"""
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.client.post(BASE_URL, json=test_wishlist.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name)
        self.assertEqual(new_wishlist["customer_id"], test_wishlist.customer_id)
        self.assertEqual(new_wishlist["description"], test_wishlist.description)

        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_wishlist = response.get_json()
        self.assertEqual(new_wishlist["name"], test_wishlist.name)
        self.assertEqual(new_wishlist["customer_id"], test_wishlist.customer_id)
        self.assertEqual(new_wishlist["description"], test_wishlist.description)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "DATABASE_URI",
            "postgresql+psycopg://postgres:postgres@localhost:5432/testdb",
        )
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_create_wishlist_no_data(self):
        """It should not Create a Wishlist with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wishlist_no_content_type(self):
        """It should not Create a Wishlist with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_wishlist_wrong_content_type(self):
        """It should not Create a Wishlist with the wrong content type"""
        response = self.client.post(
            BASE_URL, data="hello", content_type="text/html"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_wishlist_missing_name(self):
        """It should not Create a Wishlist with missing name"""
        test_wishlist = WishlistFactory()
        data = test_wishlist.serialize()
        del data["name"]
        response = self.client.post(BASE_URL, json=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_wishlist_missing_customer_id(self):
        """It should not Create a Wishlist with missing customer_id"""
        test_wishlist = WishlistFactory()
        data = test_wishlist.serialize()
        del data["customer_id"]
        response = self.client.post(BASE_URL, json=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
