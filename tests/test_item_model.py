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
# pylint: disable=duplicate-code

"""
Test cases for Item Model
"""

import logging
import os
from unittest import TestCase
from wsgi import app
from service.models import Wishlist, Item, DataValidationError, db
from tests.factories import WishlistFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


class TestItem(TestCase):
    """Item Model Test Cases"""

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

    def test_add_an_item(self):
        """It should create an Item and add it to the database"""
        wishlist = WishlistFactory()
        wishlist.create()

        item = ItemFactory(wishlist_id=wishlist.id)
        item.create()

        found_item = Item.find(item.id)
        self.assertEqual(found_item.wishlist_id, wishlist.id)
        self.assertEqual(found_item.product_id, item.product_id)
        self.assertEqual(found_item.product_name, item.product_name)
        self.assertEqual(found_item.quantity, item.quantity)
        self.assertEqual(found_item.variant_id, item.variant_id)

    def test_update_an_item(self):
        """It should update an Item"""
        wishlist = WishlistFactory()
        wishlist.create()

        item = ItemFactory(wishlist_id=wishlist.id, product_name="old")
        item.create()

        item = Item.find(item.id)
        item.product_name = "new"
        item.quantity = 3
        item.update()

        item = Item.find(item.id)
        self.assertEqual(item.product_name, "new")
        self.assertEqual(item.quantity, 3)

    def test_delete_an_item(self):
        """It should delete an Item"""
        wishlist = WishlistFactory()
        wishlist.create()

        item = ItemFactory(wishlist_id=wishlist.id)
        item.create()
        self.assertIsNotNone(item.id)

        item.delete()
        self.assertIsNone(Item.find(item.id))

    def test_serialize_an_item(self):
        """It should serialize an Item"""
        wishlist = WishlistFactory()
        wishlist.create()

        item = ItemFactory(wishlist_id=wishlist.id)
        serial = item.serialize()

        self.assertEqual(serial["id"], item.id)
        self.assertEqual(serial["wishlist_id"], item.wishlist_id)
        self.assertEqual(serial["product_id"], item.product_id)
        self.assertEqual(serial["product_name"], item.product_name)
        self.assertEqual(serial["quantity"], item.quantity)
        self.assertEqual(serial["variant_id"], item.variant_id)

    def test_deserialize_an_item(self):
        """It should deserialize an Item"""
        wishlist = WishlistFactory()
        wishlist.create()

        item = ItemFactory(wishlist_id=wishlist.id)
        new_item = Item()
        new_item.deserialize(item.serialize())

        self.assertEqual(new_item.wishlist_id, item.wishlist_id)
        self.assertEqual(new_item.product_id, item.product_id)
        self.assertEqual(new_item.product_name, item.product_name)
        self.assertEqual(new_item.quantity, item.quantity)
        self.assertEqual(new_item.variant_id, item.variant_id)

    def test_deserialize_item_key_error(self):
        """It should not deserialize an Item with missing fields"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, {})

    def test_deserialize_item_type_error(self):
        """It should not deserialize an Item with bad type"""
        item = Item()
        self.assertRaises(DataValidationError, item.deserialize, [])

    def test_deserialize_item_invalid_datetime(self):
        """It should not deserialize an Item with invalid datetime"""
        item = Item()
        data = {
            "wishlist_id": 1,
            "product_id": "SKU-1",
            "product_name": "Test",
            "quantity": 1,
            "variant_id": "VAR-1",
            "added_at": "not-a-valid-datetime",
        }
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_find_by_wishlist_id_and_product_name(self):
        """It should find Items by wishlist_id and product_name"""
        wishlist = WishlistFactory()
        wishlist.create()

        matching_item = ItemFactory(wishlist_id=wishlist.id, product_name="Sneakers")
        matching_item.create()
        ItemFactory(wishlist_id=wishlist.id, product_name="Backpack").create()

        results = Item.find_by_wishlist_id_and_product_name(wishlist.id, "Sneakers")
        self.assertEqual(results.count(), 1)
        self.assertEqual(results[0].id, matching_item.id)
        self.assertEqual(results[0].product_name, "Sneakers")
