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
from tests.factories import WishlistFactory, ItemFactory

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

    def _create_wishlists(self, count: int = 1) -> list:
        """Helper method to create test wishlists"""
        wishlists = []  # 这里的 wishlists 前面有 8 个空格
        for _ in range(count):
            test_wishlist = WishlistFactory()
            test_wishlist.create()
            wishlists.append(test_wishlist)
        return wishlists
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
            """It should call the home page and receive JSON"""
            resp = self.client.get("/")
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            data = resp.get_json()
            self.assertEqual(data["name"], "Wishlist Service") 

    # Todo: Add your test cases here...
    def test_404_not_found(self):
        """It should return 404 for invalid routes and return JSON"""
        resp = self.client.get("/invalid_route")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_wishlist(self):
        """It should Delete a Wishlist"""
        test_wishlist = self._create_wishlists(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        deleted_wishlist = Wishlist.find(test_wishlist.id)
        self.assertIsNone(deleted_wishlist)

    def test_delete_non_existing_wishlist(self):
        """It should Delete a Wishlist even if it does not exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

    
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

    # ----------------------------------------------------------
    # TEST READ WISHLIST
    # ----------------------------------------------------------
    def test_get_wishlist_with_no_items(self):
        """It should Read an existing Wishlist with no items"""
        wishlist = WishlistFactory()
        wishlist.create()

        response = self.client.get(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["id"], wishlist.id)
        self.assertEqual(data["name"], wishlist.name)
        self.assertEqual(data["customer_id"], wishlist.customer_id)
        self.assertEqual(data["description"], wishlist.description)
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 0)

    def test_get_wishlist_with_two_items(self):
        """It should Read an existing Wishlist with two items"""
        wishlist = WishlistFactory()
        wishlist.create()

        ItemFactory(
            wishlist_id=wishlist.id,
            product_name="Sneakers",
        ).create()
        ItemFactory(
            wishlist_id=wishlist.id,
            product_name="Backpack",
        ).create()

        response = self.client.get(f"{BASE_URL}/{wishlist.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["id"], wishlist.id)
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 2)

        for item in data["items"]:
            self.assertIn("product_name", item)

    def test_get_wishlist_not_found(self):
        """It should return 404 when a Wishlist is missing"""
        response = self.client.get(f"{BASE_URL}/999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("message", data)

    # ----------------------------------------------------------
    # TEST LIST ITEMS IN A WISHLIST
    # ----------------------------------------------------------
    def test_list_items_in_wishlist_with_two_items(self):
        """It should list all Items in an existing Wishlist with two items"""
        wishlist = WishlistFactory()
        wishlist.create()

        ItemFactory(wishlist_id=wishlist.id, product_name="Sneakers").create()
        ItemFactory(wishlist_id=wishlist.id, product_name="Backpack").create()

        response = self.client.get(f"{BASE_URL}/{wishlist.id}/items")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 2)

        for item in data:
            self.assertEqual(item["wishlist_id"], wishlist.id)

    def test_list_items_in_wishlist_with_zero_items(self):
        """It should return an empty list when the Wishlist has no items"""
        wishlist = WishlistFactory()
        wishlist.create()

        response = self.client.get(f"{BASE_URL}/{wishlist.id}/items")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data, [])

    def test_list_items_in_wishlist_not_found(self):
        """It should return 404 when listing items for a missing Wishlist"""
        response = self.client.get(f"{BASE_URL}/999999/items")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("message", data)

    # ----------------------------------------------------------
    # TEST CREATE ITEM IN A WISHLIST
    # ----------------------------------------------------------
    def test_create_item_in_wishlist(self):
        """It should Create an Item in a Wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()
        test_item = ItemFactory(wishlist_id=wishlist.id)
        item_data = {
            "product_id": test_item.product_id,
            "product_name": test_item.product_name,
            "quantity": test_item.quantity,
            "variant_id": test_item.variant_id,
        }
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items", json=item_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_item = response.get_json()
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        self.assertIn(str(new_item["id"]), location)
        self.assertEqual(new_item["wishlist_id"], wishlist.id)
        self.assertEqual(new_item["product_id"], test_item.product_id)
        self.assertEqual(new_item["product_name"], test_item.product_name)
        self.assertEqual(new_item["variant_id"], test_item.variant_id)

        response = self.client.get(f"{BASE_URL}/{wishlist.id}/items")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["product_name"], test_item.product_name)

    def test_create_item_wishlist_not_found(self):
        """It should return 404 when creating an Item in a missing Wishlist"""
        test_item = ItemFactory()
        item_data = {
            "product_id": test_item.product_id,
            "product_name": test_item.product_name,
            "quantity": test_item.quantity,
            "variant_id": test_item.variant_id,
        }
        response = self.client.post(
            f"{BASE_URL}/999999/items", json=item_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        self.assertIn("message", data)

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_create_wishlist(self):
        """It should Create a new Wishlist"""
        test_wishlist = WishlistFactory()
        logging.debug("Test Wishlist: %s", test_wishlist.serialize())
        response = self.client.post(BASE_URL, json=test_wishlist.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_wishlist = response.get_json()
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        self.assertIn(str(new_wishlist["id"]), location)
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
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
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

    def test_create_item_no_data(self):
        """It should not Create an Item with missing data"""
        wishlist = WishlistFactory()
        wishlist.create()
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items", json={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_no_content_type(self):
        """It should not Create an Item with no content type"""
        wishlist = WishlistFactory()
        wishlist.create()
        response = self.client.post(f"{BASE_URL}/{wishlist.id}/items")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_item_wrong_content_type(self):
        """It should not Create an Item with the wrong content type"""
        wishlist = WishlistFactory()
        wishlist.create()
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items",
            data="hello",
            content_type="text/html",
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_item_missing_product_id(self):
        """It should not Create an Item with missing product_id"""
        wishlist = WishlistFactory()
        wishlist.create()
        test_item = ItemFactory(wishlist_id=wishlist.id)
        item_data = {
            "product_name": test_item.product_name,
            "quantity": test_item.quantity,
            "variant_id": test_item.variant_id,
        }
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items", json=item_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_missing_product_name(self):
        """It should not Create an Item with missing product_name"""
        wishlist = WishlistFactory()
        wishlist.create()
        test_item = ItemFactory(wishlist_id=wishlist.id)
        item_data = {
            "product_id": test_item.product_id,
            "quantity": test_item.quantity,
            "variant_id": test_item.variant_id,
        }
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items", json=item_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_missing_variant_id(self):
        """It should not Create an Item with missing variant_id"""
        wishlist = WishlistFactory()
        wishlist.create()
        test_item = ItemFactory(wishlist_id=wishlist.id)
        item_data = {
            "product_id": test_item.product_id,
            "product_name": test_item.product_name,
            "quantity": test_item.quantity,
        }
        response = self.client.post(
            f"{BASE_URL}/{wishlist.id}/items", json=item_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
