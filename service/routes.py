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
Wishlist Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Wishlist
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Wishlist, Item
from service.common import status  # HTTP Status Codes
from service.landing import get_landing_html


######################################################################
# GET INDEX
######################################################################
def _index_json():
    return jsonify(
        name="Wishlist REST API Service",
        version="1.0",
        message="Wishlist service is up",
        paths=url_for("list_wishlists", _external=True),
        endpoints={
            "Wishlists": [
                {
                    "method": "GET",
                    "path": "/wishlists",
                    "description": "List wishlists (supports ?customer_id=, ?name=, ?description=)",
                },
                {"method": "POST", "path": "/wishlists", "description": "Create a wishlist"},
                {"method": "GET", "path": "/wishlists/{wishlist_id}", "description": "Get one wishlist"},
                {"method": "PUT", "path": "/wishlists/{wishlist_id}", "description": "Update wishlist name/description"},
                {"method": "DELETE", "path": "/wishlists/{wishlist_id}", "description": "Delete a wishlist"},
            ],
            "Wishlist Items": [
                {
                    "method": "GET",
                    "path": "/wishlists/{wishlist_id}/items",
                    "description": "List items in a wishlist (supports ?product_name=)",
                },
                {"method": "POST", "path": "/wishlists/{wishlist_id}/items",
                 "description": "Create an item in a wishlist"},
                {"method": "GET", "path": "/wishlists/{wishlist_id}/items/{item_id}",
                 "description": "Get one item in a wishlist"},
                {"method": "PUT", "path": "/wishlists/{wishlist_id}/items/{item_id}",
                 "description": "Update item in wishlist"},
                {"method": "DELETE", "path": "/wishlists/{wishlist_id}/items/{item_id}",
                 "description": "Delete item from wishlist"},
            ],
        },
    ), status.HTTP_200_OK


def _index_html():
    return get_landing_html(), status.HTTP_200_OK, {"Content-Type": "text/html; charset=utf-8"}


@app.route("/")
def index():
    """Root URL response – HTML landing page or JSON for API clients"""
    app.logger.info("Request for Root URL")
    if "application/json" in request.headers.get("Accept", ""):
        return _index_json()
    return _index_html()


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# LIST ALL WISHLISTS
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """Returns all of the Wishlists, optionally filtered by query params"""
    app.logger.info("Request for wishlist list")

    wishlists = []
    customer_id = request.args.get("customer_id")
    name = request.args.get("name")
    description = request.args.get("description")

    if customer_id:
        app.logger.info("Filtering by customer_id: %s", customer_id)
        try:
            customer_id = int(customer_id)
        except ValueError:
            abort(status.HTTP_400_BAD_REQUEST, f"Invalid customer_id: {customer_id}")
        wishlists = Wishlist.find_by_customer_id(customer_id)
    elif name:
        app.logger.info("Filtering by name: %s", name)
        wishlists = Wishlist.find_by_name(name)
    elif description:
        app.logger.info("Filtering by description: %s", description)
        wishlists = Wishlist.find_by_description(description)
    else:
        app.logger.info("Returning all wishlists")
        wishlists = Wishlist.all()

    results = [wishlist.serialize() for wishlist in wishlists]
    app.logger.info("Returning %d wishlists", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# READ A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlist(wishlist_id):
    """Retrieve a single Wishlist by its ID"""
    app.logger.info("Request to Retrieve a wishlist with id [%s]", wishlist_id)

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' not found.")

    return jsonify(wishlist.serialize()), status.HTTP_200_OK


######################################################################
# LIST ITEMS IN A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["GET"])
def list_wishlist_items(wishlist_id):
    """List all items belonging to a specific Wishlist"""
    app.logger.info("Request to list items for wishlist id [%s]", wishlist_id)

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' not found.")

    product_name = request.args.get("product_name")
    if product_name:
        app.logger.info("Filtering items by product_name: %s", product_name)
        items = Item.find_by_wishlist_id_and_product_name(wishlist_id, product_name)
    else:
        items = wishlist.items

    results = [item.serialize() for item in items]
    return jsonify(results), status.HTTP_200_OK


######################################################################
# READ AN ITEM IN A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["GET"])
def get_wishlist_item(wishlist_id, item_id):
    """Retrieve a single Item from a Wishlist by its ID"""
    app.logger.info(
        "Request to Retrieve item %s from wishlist %s", item_id, wishlist_id
    )

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' not found.")

    item = Item.find(item_id)
    if not item or item.wishlist_id != wishlist_id:
        abort(status.HTTP_404_NOT_FOUND, f"Item with id '{item_id}' not found.")

    app.logger.info("Returning item: %s", item.product_name)
    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
# CREATE ITEM IN A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["POST"])
def create_wishlist_items(wishlist_id):
    """
    Create an Item in a Wishlist
    This endpoint will create an Item in the specified Wishlist
    """
    app.logger.info("Request to Create an Item in wishlist id [%s]", wishlist_id)

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' not found.")

    check_content_type("application/json")

    data = request.get_json()
    data["wishlist_id"] = wishlist_id
    app.logger.info("Processing: %s", data)

    # Check for duplicate (wishlist_id, product_id, variant_id)
    existing = Item.find_by_wishlist_product_variant(
        wishlist_id, data.get("product_id"), data.get("variant_id")
    )
    if existing:
        abort(
            status.HTTP_409_CONFLICT,
            f"Item with product_id '{data.get('product_id')}' and "
            f"variant_id '{data.get('variant_id')}' already exists in wishlist '{wishlist_id}'.",
        )

    item = Item()
    item.deserialize(data)

    item.create()
    app.logger.info("Item with new id [%s] saved!", item.id)

    location_url = (
        f"{request.url_root.rstrip('/')}/wishlists/{wishlist_id}/items/{item.id}"
    )
    return (
        jsonify(item.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# UPDATE AN ITEM IN A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["PUT"])
def update_wishlist_item(wishlist_id, item_id):
    """
    Update an Item in a Wishlist

    This endpoint will update an Item in the specified Wishlist
    """
    app.logger.info(
        "Request to Update item %s in wishlist %s", item_id, wishlist_id
    )

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' not found.",
        )

    item = Item.find(item_id)
    if not item or item.wishlist_id != wishlist_id:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Item with id '{item_id}' not found in wishlist '{wishlist_id}'.",
        )

    check_content_type("application/json")

    data = request.get_json()
    data["wishlist_id"] = wishlist_id
    app.logger.info("Processing: %s", data)
    item.deserialize(data)
    item.update()

    app.logger.info("Item with id [%s] updated.", item.id)
    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
# CREATE A NEW WISHLIST
######################################################################
@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """
    Create a Wishlist
    This endpoint will create a Wishlist based the data in the body that is posted
    """
    app.logger.info("Request to Create a Wishlist...")
    check_content_type("application/json")

    wishlist = Wishlist()
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    wishlist.deserialize(data)

    wishlist.create()
    app.logger.info("Wishlist with new id [%s] saved!", wishlist.id)

    location_url = f"{request.url_root.rstrip('/')}/wishlists/{wishlist.id}"
    return (
        jsonify(wishlist.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# DELETE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    """
    Delete a Wishlist

    This endpoint will delete a Wishlist based the id specified in the path
    """
    app.logger.info("Request to Delete a wishlist with id [%s]", wishlist_id)

    # Delete the Wishlist if it exists
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        app.logger.info("Wishlist with ID: %d found.", wishlist.id)
        wishlist.delete()

    app.logger.info("Wishlist with ID: %d delete complete.", wishlist_id)
    return {}, status.HTTP_204_NO_CONTENT


######################################################################
# DELETE AN ITEM FROM A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["DELETE"])
def delete_wishlist_item(wishlist_id, item_id):
    """
    Delete an Item from a Wishlist

    This endpoint will delete an Item from the specified Wishlist
    """
    app.logger.info("Request to Delete item %s from wishlist %s", item_id, wishlist_id)

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' not found.",
        )

    item = Item.find(item_id)
    if not item or item.wishlist_id != wishlist_id:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Item with id '{item_id}' not found in wishlist '{wishlist_id}'.",
        )

    item.delete()
    app.logger.info("Item with ID: %d deleted.", item_id)
    return {}, status.HTTP_204_NO_CONTENT


@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlists(wishlist_id):
    """
    Update a Wishlist

    This endpoint will update a Wishlist based the body that is posted
    """
    app.logger.info("Request to update wishlist with id: %s", wishlist_id)
    check_content_type("application/json")

    # See if the wishlist exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' was not found.",
        )

    data = request.get_json()

    if not data or "name" not in data:
        abort(
            status.HTTP_400_BAD_REQUEST,
            "Wishlist must have a name",
        )
    if not isinstance(data["name"], str) or not data["name"].strip():
        abort(
            status.HTTP_400_BAD_REQUEST,
            "Wishlist must have a valid name",
        )
    wishlist.name = data["name"].strip()

    if "description" in data:
        if not isinstance(data["description"], str):
            abort(
                status.HTTP_400_BAD_REQUEST,
                "Wishlist must have a valid description",
            )
        wishlist.description = data["description"].strip()

    wishlist.update()

    return jsonify(wishlist.serialize()), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
