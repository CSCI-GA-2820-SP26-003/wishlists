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
# pylint: disable=duplicate-code,too-many-public-methods

"""
Test cases for Wishlist Model
"""

import logging
import os
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import Wishlist, Item, DataValidationError, db
from tests.factories import WishlistFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


class TestWishlist(TestCase):
    """Wishlist Model Test Cases"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Item).delete()
        db.session.query(Wishlist).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def test_create_a_wishlist(self):
        """It should Create a Wishlist and assert that it exists"""
        wishlist = WishlistFactory()
        self.assertIsNotNone(wishlist)
        self.assertIsNotNone(wishlist.id)
        self.assertIsNotNone(wishlist.name)
        self.assertIsNotNone(wishlist.customer_id)

    def test_add_a_wishlist(self):
        """It should Create a wishlist and add it to the database"""
        wishlists = Wishlist.all()
        self.assertEqual(wishlists, [])
        wishlist = WishlistFactory()
        wishlist.create()
        self.assertIsNotNone(wishlist.id)
        wishlists = Wishlist.all()
        self.assertEqual(len(wishlists), 1)

    @patch("service.models.db.session.commit")
    def test_add_wishlist_failed(self, exception_mock):
        """It should not create a Wishlist on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistFactory()
        self.assertRaises(DataValidationError, wishlist.create)

    def test_read_a_wishlist(self):
        """It should Read a Wishlist"""
        wishlist = WishlistFactory()
        wishlist.create()

        found_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(found_wishlist.id, wishlist.id)
        self.assertEqual(found_wishlist.name, wishlist.name)
        self.assertEqual(found_wishlist.customer_id, wishlist.customer_id)
        self.assertEqual(found_wishlist.description, wishlist.description)

    def test_update_a_wishlist(self):
        """It should Update a Wishlist"""
        wishlist = WishlistFactory(description="old")
        wishlist.create()
        self.assertEqual(wishlist.description, "old")

        wishlist = Wishlist.find(wishlist.id)
        wishlist.description = "new"
        wishlist.update()

        wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(wishlist.description, "new")

    @patch("service.models.db.session.commit")
    def test_update_wishlist_failed(self, exception_mock):
        """It should not update a Wishlist on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistFactory()
        self.assertRaises(DataValidationError, wishlist.update)

    def test_delete_a_wishlist(self):
        """It should Delete a wishlist from the database"""
        wishlist = WishlistFactory()
        wishlist.create()
        self.assertIsNotNone(wishlist.id)
        self.assertEqual(len(Wishlist.all()), 1)

        wishlist.delete()
        self.assertEqual(len(Wishlist.all()), 0)

    @patch("service.models.db.session.commit")
    def test_delete_wishlist_failed(self, exception_mock):
        """It should not delete a Wishlist on database error"""
        exception_mock.side_effect = Exception()
        wishlist = WishlistFactory()
        self.assertRaises(DataValidationError, wishlist.delete)

    def test_list_all_wishlists(self):
        """It should List all Wishlists in the database"""
        self.assertEqual(Wishlist.all(), [])
        for wishlist in WishlistFactory.create_batch(5):
            wishlist.create()
        self.assertEqual(len(Wishlist.all()), 5)

    def test_find_by_name(self):
        """It should Find a Wishlist by name"""
        wishlist = WishlistFactory()
        wishlist.create()

        same_wishlist = Wishlist.find_by_name(wishlist.name)[0]
        self.assertEqual(same_wishlist.id, wishlist.id)
        self.assertEqual(same_wishlist.name, wishlist.name)

    def test_find_by_customer_id(self):
        """It should Find Wishlists by customer_id"""
        wishlist = WishlistFactory()
        wishlist.create()

        results = Wishlist.find_by_customer_id(wishlist.customer_id)
        self.assertEqual(results[0].id, wishlist.id)
        self.assertEqual(results[0].customer_id, wishlist.customer_id)

    def test_serialize_a_wishlist(self):
        """It should serialize a Wishlist"""
        wishlist = WishlistFactory()
        item = ItemFactory(wishlist_id=wishlist.id)
        wishlist.items.append(item)

        serial = wishlist.serialize()
        self.assertEqual(serial["id"], wishlist.id)
        self.assertEqual(serial["name"], wishlist.name)
        self.assertEqual(serial["customer_id"], wishlist.customer_id)
        self.assertEqual(serial["description"], wishlist.description)
        self.assertEqual(len(serial["items"]), 1)

    def test_deserialize_a_wishlist(self):
        """It should deserialize a Wishlist"""
        wishlist = WishlistFactory()
        serial = wishlist.serialize()

        new_wishlist = Wishlist()
        new_wishlist.deserialize(serial)
        self.assertEqual(new_wishlist.name, wishlist.name)
        self.assertEqual(new_wishlist.customer_id, wishlist.customer_id)
        self.assertEqual(new_wishlist.description, wishlist.description)

    def test_deserialize_with_key_error(self):
        """It should not deserialize a Wishlist with a KeyError"""
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, {})

    def test_deserialize_with_type_error(self):
        """It should not deserialize a Wishlist with a TypeError"""
        wishlist = Wishlist()
        self.assertRaises(DataValidationError, wishlist.deserialize, [])

    def test_deserialize_wishlist_invalid_datetime(self):
        """It should not deserialize a Wishlist with invalid datetime"""
        wishlist = Wishlist()
        data = {
            "name": "Test",
            "customer_id": 1,
            "description": "Test",
            "created_at": "not-a-valid-datetime",
        }
        self.assertRaises(DataValidationError, wishlist.deserialize, data)

    def test_create_item_for_wishlist_relationship(self):
        """It should create an Item and load it through Wishlist.items"""
        wishlist = WishlistFactory()
        wishlist.create()

        item = ItemFactory(wishlist_id=wishlist.id)
        item.create()

        found_wishlist = Wishlist.find(wishlist.id)
        self.assertEqual(len(found_wishlist.items), 1)
        self.assertEqual(found_wishlist.items[0].id, item.id)
