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
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_wishlists(self, count):
        """Factory method to create wishlists in bulk"""
        wishlists = []
        for _ in range(count):
            wishlist = WishlistFactory()
            wishlist.create()
            wishlists.append(wishlist)
        return wishlists

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # ----------------------------------------------------------
    # TEST LIST ALL WISHLISTS
    # ----------------------------------------------------------

    def test_list_all_wishlists(self):
        """It should List all Wishlists"""
        self._create_wishlists(5)
        resp = self.client.get("/wishlists")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_list_wishlists_by_customer_id(self):
        """It should List Wishlists filtered by customer_id"""
        wishlists = self._create_wishlists(3)
        target = wishlists[0]
        resp = self.client.get(f"/wishlists?customer_id={target.customer_id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        for wl in data:
            self.assertEqual(wl["customer_id"], target.customer_id)

    def test_list_wishlists_by_customer_id_no_results(self):
        """It should return an empty list when customer_id has no wishlists"""
        self._create_wishlists(3)
        resp = self.client.get("/wishlists?customer_id=0")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)

    def test_list_wishlists_by_name(self):
        """It should List Wishlists filtered by name"""
        wishlists = self._create_wishlists(3)
        target = wishlists[0]
        resp = self.client.get(f"/wishlists?name={target.name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        for wl in data:
            self.assertEqual(wl["name"], target.name)

    def test_list_all_wishlists_empty(self):
        """It should return an empty list when no Wishlists exist"""
        resp = self.client.get("/wishlists")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)

    def test_list_wishlists_bad_customer_id(self):
        """It should return 400 when customer_id is not a valid integer"""
        resp = self.client.get("/wishlists?customer_id=abc")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
