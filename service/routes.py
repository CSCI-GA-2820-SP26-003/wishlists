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
Wishlist Service with Flask-RESTX and Swagger
"""

from flask import jsonify, request
from flask import current_app as app  # Import Flask application
from flask_restx import Api, Resource, fields
from werkzeug.exceptions import HTTPException
from service.models import Wishlist, Item, DataValidationError
from service.common import status  # HTTP Status Codes
from service.demo_ui import get_demo_html

ERROR_TITLES = {
    status.HTTP_400_BAD_REQUEST: "Bad Request",
    status.HTTP_404_NOT_FOUND: "Not Found",
    status.HTTP_405_METHOD_NOT_ALLOWED: "Method not Allowed",
    status.HTTP_409_CONFLICT: "Conflict",
    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: "Unsupported media type",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
}

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(
    app,
    version="1.0.0",
    title="Wishlist REST API Service",
    description="Manage wishlists and wishlist items.",
    default="wishlists",
    default_label="Wishlist operations",
    doc="/apidocs/",
    prefix="/api",
)

create_wishlist_model = api.model(
    "WishlistCreate",
    {
        "name": fields.String(required=True, description="The wishlist name"),
        "customer_id": fields.Integer(required=True, description="The owning customer id"),
        "description": fields.String(required=False, description="Optional wishlist description"),
    },
)

update_wishlist_model = api.model(
    "WishlistUpdate",
    {
        "name": fields.String(required=True, description="The updated wishlist name"),
        "description": fields.String(required=False, description="The updated wishlist description"),
    },
)

create_item_model = api.model(
    "ItemCreate",
    {
        "product_id": fields.String(required=True, description="The product identifier"),
        "product_name": fields.String(required=True, description="The product name"),
        "quantity": fields.Integer(required=False, description="The desired quantity", default=1),
        "variant_id": fields.String(required=True, description="The product variant identifier"),
    },
)

item_model = api.inherit(
    "Item",
    create_item_model,
    {
        "id": fields.Integer(readOnly=True, description="The unique item identifier"),
        "wishlist_id": fields.Integer(readOnly=True, description="The parent wishlist identifier"),
        "added_at": fields.String(readOnly=True, description="The item creation timestamp"),
        "updated_at": fields.String(readOnly=True, description="The item update timestamp"),
    },
)

wishlist_model = api.inherit(
    "Wishlist",
    create_wishlist_model,
    {
        "id": fields.Integer(readOnly=True, description="The unique wishlist identifier"),
        "is_private": fields.Boolean(readOnly=True, description="Whether the wishlist is private"),
        "created_at": fields.String(readOnly=True, description="The wishlist creation timestamp"),
        "updated_at": fields.String(readOnly=True, description="The wishlist update timestamp"),
        "items": fields.List(fields.Nested(item_model), readOnly=True, description="Wishlist items"),
    },
)

health_model = api.model(
    "HealthStatus",
    {
        "status": fields.String(required=True, description="The service health state"),
    },
)


def api_error_response(status_code, message, error_title=None, **kwargs):
    """Build a standard JSON error response."""
    payload = {
        "status": status_code,
        "error": error_title or ERROR_TITLES.get(status_code, "Error"),
        "message": message,
    }
    payload.update(kwargs)
    return payload, status_code


@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """Handles validation errors from bad data on API routes."""
    message = str(error)
    app.logger.warning(message)
    return api_error_response(status.HTTP_400_BAD_REQUEST, message)


@api.errorhandler(HTTPException)
def http_exception_handler(error):
    """Handles HTTP errors for API routes."""
    status_code = getattr(error, "code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    data = dict(getattr(error, "data", {}) or {})
    message = data.pop("message", None) or getattr(error, "description", str(error))
    error_title = data.pop("error", ERROR_TITLES.get(status_code, "Error"))
    status_value = data.pop("status", status_code)
    app.logger.warning(message)
    return api_error_response(status_value, message, error_title, **data)


@api.errorhandler(Exception)
def default_error_handler(error):
    """Handles unexpected errors for API routes."""
    message = str(error) or ERROR_TITLES[status.HTTP_500_INTERNAL_SERVER_ERROR]
    app.logger.error(message)
    return api_error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message)


def api_url(path):
    """Build an absolute API URL for the current request."""
    return f"{request.url_root.rstrip('/')}{path}"


def abort(error_code, message, **kwargs):
    """Logs errors before aborting."""
    app.logger.error(message)
    api.abort(
        error_code,
        message=message,
        error=ERROR_TITLES.get(error_code, "Error"),
        status=error_code,
        **kwargs,
    )


######################################################################
# GET INDEX
######################################################################
def _index_json():
    return (
        jsonify(
            name="Wishlist REST API Service",
            version="1.0",
            message="Wishlist service is up",
            paths=api_url("/api/wishlists"),
            docs=api_url("/apidocs/"),
            endpoints={
                "Service": [
                    {"method": "GET", "path": "/api/health", "description": "Health check"},
                    {"method": "GET", "path": "/apidocs/", "description": "Swagger UI"},
                ],
                "Wishlists": [
                    {
                        "method": "GET",
                        "path": "/api/wishlists",
                        "description": "List wishlists (supports ?customer_id=, ?name=, ?description=)",
                    },
                    {"method": "POST", "path": "/api/wishlists", "description": "Create a wishlist"},
                    {"method": "GET", "path": "/api/wishlists/{wishlist_id}", "description": "Get one wishlist"},
                    {
                        "method": "PUT",
                        "path": "/api/wishlists/{wishlist_id}",
                        "description": "Update wishlist name/description",
                    },
                    {
                        "method": "DELETE",
                        "path": "/api/wishlists/{wishlist_id}",
                        "description": "Delete a wishlist",
                    },
                    {
                        "method": "POST",
                        "path": "/api/wishlists/{wishlist_id}/private",
                        "description": "Action: set wishlist privacy to private",
                    },
                ],
                "Wishlist Items": [
                    {
                        "method": "GET",
                        "path": "/api/wishlists/{wishlist_id}/items",
                        "description": "List items in a wishlist (supports ?product_name=)",
                    },
                    {
                        "method": "POST",
                        "path": "/api/wishlists/{wishlist_id}/items",
                        "description": "Create an item in a wishlist",
                    },
                    {
                        "method": "GET",
                        "path": "/api/wishlists/{wishlist_id}/items/{item_id}",
                        "description": "Get one item in a wishlist",
                    },
                    {
                        "method": "PUT",
                        "path": "/api/wishlists/{wishlist_id}/items/{item_id}",
                        "description": "Update item in wishlist",
                    },
                    {
                        "method": "DELETE",
                        "path": "/api/wishlists/{wishlist_id}/items/{item_id}",
                        "description": "Delete item from wishlist",
                    },
                ],
            },
        ),
        status.HTTP_200_OK,
    )


@app.route("/")
def index():
    """Root URL response - HTML landing page or JSON for API clients."""
    app.logger.info("Request for Root URL")
    if "application/json" in request.headers.get("Accept", ""):
        return _index_json()
    return app.send_static_file("index.html")


@app.route("/health", methods=["GET"])
def healthcheck():
    """Health endpoint for liveness and readiness probes."""
    return jsonify({"status": "OK"}), status.HTTP_200_OK


@app.route("/demo", methods=["GET"])
def demo():
    """Simple HTML demo page to exercise the API."""
    return get_demo_html(), status.HTTP_200_OK, {"Content-Type": "text/html; charset=utf-8"}


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# LIST ALL WISHLISTS
######################################################################
def list_wishlists():
    """Returns all of the Wishlists, optionally filtered by query params."""
    app.logger.info("Request for wishlist list")

    wishlists = []
    customer_id = request.args.get("customer_id")
    name = request.args.get("name")
    description = request.args.get("description")

    if customer_id:
        app.logger.info("Filtering by customer_id: %s", customer_id)
        try:
            customer_id = int(customer_id)
        except ValueError as error:
            raise DataValidationError(f"Invalid customer_id: {customer_id}") from error
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
    return results, status.HTTP_200_OK


######################################################################
# READ A WISHLIST
######################################################################
def get_wishlist(wishlist_id):
    """Retrieve a single Wishlist by its ID."""
    app.logger.info("Request to Retrieve a wishlist with id [%s]", wishlist_id)

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' not found.")

    return wishlist.serialize(), status.HTTP_200_OK


######################################################################
# ACTION: SET WISHLIST TO PRIVATE
######################################################################
def set_wishlist_private(wishlist_id):
    """Action: mark a wishlist as private (not a generic CRUD update)."""
    app.logger.info("Request to set wishlist id [%s] to private", wishlist_id)
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' not found.",
        )
    wishlist.is_private = True
    wishlist.update()
    return wishlist.serialize(), status.HTTP_200_OK


######################################################################
# LIST ITEMS IN A WISHLIST
######################################################################
def list_wishlist_items(wishlist_id):
    """List all items belonging to a specific Wishlist."""
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
    return results, status.HTTP_200_OK


######################################################################
# READ AN ITEM IN A WISHLIST
######################################################################
def get_wishlist_item(wishlist_id, item_id):
    """Retrieve a single Item from a Wishlist by its ID."""
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
    return item.serialize(), status.HTTP_200_OK


######################################################################
# CREATE ITEM IN A WISHLIST
######################################################################
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

    data = request.get_json() or {}
    data["wishlist_id"] = wishlist_id
    app.logger.info("Processing: %s", data)

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

    location_url = f"{request.url_root.rstrip('/')}/api/wishlists/{wishlist_id}/items/{item.id}"
    return (
        item.serialize(),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# UPDATE AN ITEM IN A WISHLIST
######################################################################
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

    data = request.get_json() or {}
    data["wishlist_id"] = wishlist_id
    app.logger.info("Processing: %s", data)
    item.deserialize(data)
    item.update()

    app.logger.info("Item with id [%s] updated.", item.id)
    return item.serialize(), status.HTTP_200_OK


######################################################################
# CREATE A NEW WISHLIST
######################################################################
def create_wishlists():
    """
    Create a Wishlist
    This endpoint will create a Wishlist based the data in the body that is posted
    """
    app.logger.info("Request to Create a Wishlist...")
    check_content_type("application/json")

    wishlist = Wishlist()
    data = request.get_json() or {}
    app.logger.info("Processing: %s", data)
    wishlist.deserialize(data)

    wishlist.create()
    app.logger.info("Wishlist with new id [%s] saved!", wishlist.id)

    location_url = f"{request.url_root.rstrip('/')}/api/wishlists/{wishlist.id}"
    return (
        wishlist.serialize(),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# DELETE A WISHLIST
######################################################################
def delete_wishlists(wishlist_id):
    """
    Delete a Wishlist

    This endpoint will delete a Wishlist based the id specified in the path
    """
    app.logger.info("Request to Delete a wishlist with id [%s]", wishlist_id)

    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        app.logger.info("Wishlist with ID: %d found.", wishlist.id)
        wishlist.delete()

    app.logger.info("Wishlist with ID: %d delete complete.", wishlist_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# DELETE AN ITEM FROM A WISHLIST
######################################################################
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
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# UPDATE A WISHLIST
######################################################################
def update_wishlists(wishlist_id):
    """
    Update a Wishlist

    This endpoint will update a Wishlist based the body that is posted
    """
    app.logger.info("Request to update wishlist with id: %s", wishlist_id)
    check_content_type("application/json")

    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' was not found.",
        )

    data = request.get_json() or {}

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

    return wishlist.serialize(), status.HTTP_200_OK


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

    if request.mimetype == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# RESTX Resource Wrappers
######################################################################
@api.route("/health")
class HealthResource(Resource):
    """Read-only health endpoint."""

    @api.doc("health_check")
    @api.marshal_with(health_model)
    def get(self):
        """Health endpoint for API clients."""
        return {"status": "OK"}, status.HTTP_200_OK


@api.route("/wishlists", strict_slashes=False)
class WishlistCollection(Resource):
    """Handles all interactions with collections of Wishlists."""

    @api.doc(
        "list_wishlists",
        params={
            "customer_id": "Filter wishlists by customer id",
            "name": "Filter wishlists by name",
            "description": "Filter wishlists by description",
        },
    )
    @api.marshal_list_with(wishlist_model)
    def get(self):
        """Returns all of the Wishlists."""
        return list_wishlists()

    @api.doc("create_wishlists")
    @api.response(status.HTTP_400_BAD_REQUEST, "The posted wishlist data was not valid")
    @api.response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")
    @api.expect(create_wishlist_model)
    @api.marshal_with(wishlist_model, code=status.HTTP_201_CREATED)
    def post(self):
        """Creates a Wishlist."""
        return create_wishlists()


@api.route("/wishlists/<int:wishlist_id>")
@api.param("wishlist_id", "The Wishlist identifier")
class WishlistResource(Resource):
    """Allows the manipulation of a single Wishlist."""

    @api.doc("get_wishlist")
    @api.response(status.HTTP_404_NOT_FOUND, "Wishlist not found")
    @api.marshal_with(wishlist_model)
    def get(self, wishlist_id):
        """Retrieve a Wishlist with the id."""
        return get_wishlist(wishlist_id)

    @api.doc("update_wishlists")
    @api.response(status.HTTP_404_NOT_FOUND, "Wishlist not found")
    @api.response(status.HTTP_400_BAD_REQUEST, "The posted wishlist data was not valid")
    @api.response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")
    @api.expect(update_wishlist_model)
    @api.marshal_with(wishlist_model)
    def put(self, wishlist_id):
        """Update a Wishlist with the id."""
        return update_wishlists(wishlist_id)

    @api.doc("delete_wishlists")
    @api.response(status.HTTP_204_NO_CONTENT, "Wishlist deleted")
    def delete(self, wishlist_id):
        """Delete a Wishlist with the id."""
        return delete_wishlists(wishlist_id)


@api.route("/wishlists/<int:wishlist_id>/private")
@api.param("wishlist_id", "The Wishlist identifier")
class WishlistPrivateResource(Resource):
    """Wishlist action resource."""

    @api.doc("set_wishlist_private")
    @api.response(status.HTTP_404_NOT_FOUND, "Wishlist not found")
    @api.marshal_with(wishlist_model)
    def post(self, wishlist_id):
        """Set a Wishlist to private."""
        return set_wishlist_private(wishlist_id)


@api.route("/wishlists/<int:wishlist_id>/items", strict_slashes=False)
@api.param("wishlist_id", "The Wishlist identifier")
class WishlistItemCollection(Resource):
    """Handles all interactions with collections of Wishlist items."""

    @api.doc(
        "list_wishlist_items",
        params={"product_name": "Filter wishlist items by product name"},
    )
    @api.response(status.HTTP_404_NOT_FOUND, "Wishlist not found")
    @api.marshal_list_with(item_model)
    def get(self, wishlist_id):
        """Returns all of the Items in a Wishlist."""
        return list_wishlist_items(wishlist_id)

    @api.doc("create_wishlist_items")
    @api.response(status.HTTP_400_BAD_REQUEST, "The posted item data was not valid")
    @api.response(status.HTTP_404_NOT_FOUND, "Wishlist not found")
    @api.response(status.HTTP_409_CONFLICT, "Duplicate item")
    @api.response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")
    @api.expect(create_item_model)
    @api.marshal_with(item_model, code=status.HTTP_201_CREATED)
    def post(self, wishlist_id):
        """Creates an Item in a Wishlist."""
        return create_wishlist_items(wishlist_id)


@api.route("/wishlists/<int:wishlist_id>/items/<int:item_id>")
@api.param("wishlist_id", "The Wishlist identifier")
@api.param("item_id", "The Item identifier")
class WishlistItemResource(Resource):
    """Allows the manipulation of a single Wishlist item."""

    @api.doc("get_wishlist_item")
    @api.response(status.HTTP_404_NOT_FOUND, "Wishlist or item not found")
    @api.marshal_with(item_model)
    def get(self, wishlist_id, item_id):
        """Retrieve an Item from a Wishlist by its id."""
        return get_wishlist_item(wishlist_id, item_id)

    @api.doc("update_wishlist_item")
    @api.response(status.HTTP_404_NOT_FOUND, "Wishlist or item not found")
    @api.response(status.HTTP_400_BAD_REQUEST, "The posted item data was not valid")
    @api.response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Content-Type must be application/json")
    @api.expect(create_item_model)
    @api.marshal_with(item_model)
    def put(self, wishlist_id, item_id):
        """Update an Item in a Wishlist."""
        return update_wishlist_item(wishlist_id, item_id)

    @api.doc("delete_wishlist_item")
    @api.response(status.HTTP_204_NO_CONTENT, "Item deleted")
    @api.response(status.HTTP_404_NOT_FOUND, "Wishlist or item not found")
    def delete(self, wishlist_id, item_id):
        """Delete an Item from a Wishlist."""
        return delete_wishlist_item(wishlist_id, item_id)


@app.route("/wishlists", methods=["GET", "POST"])
def legacy_wishlist_collection():
    """Legacy non-RESTX collection routes kept for demo/backward compatibility."""
    if request.method == "GET":
        payload, code = list_wishlists()
        return jsonify(payload), code
    payload, code, headers = create_wishlists()
    return jsonify(payload), code, headers


@app.route("/wishlists/<int:wishlist_id>", methods=["GET", "PUT", "DELETE"])
def legacy_wishlist_resource(wishlist_id):
    """Legacy non-RESTX wishlist routes kept for demo/backward compatibility."""
    if request.method == "GET":
        payload, code = get_wishlist(wishlist_id)
        return jsonify(payload), code
    if request.method == "PUT":
        payload, code = update_wishlists(wishlist_id)
        return jsonify(payload), code
    payload, code = delete_wishlists(wishlist_id)
    return payload, code


@app.route("/wishlists/<int:wishlist_id>/private", methods=["POST"])
def legacy_wishlist_private(wishlist_id):
    """Legacy non-RESTX wishlist action route kept for compatibility."""
    payload, code = set_wishlist_private(wishlist_id)
    return jsonify(payload), code


@app.route("/wishlists/<int:wishlist_id>/items", methods=["GET", "POST"])
def legacy_wishlist_items_collection(wishlist_id):
    """Legacy non-RESTX item collection routes kept for compatibility."""
    if request.method == "GET":
        payload, code = list_wishlist_items(wishlist_id)
        return jsonify(payload), code
    payload, code, headers = create_wishlist_items(wishlist_id)
    return jsonify(payload), code, headers


@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["GET", "PUT", "DELETE"])
def legacy_wishlist_item_resource(wishlist_id, item_id):
    """Legacy non-RESTX item routes kept for compatibility."""
    if request.method == "GET":
        payload, code = get_wishlist_item(wishlist_id, item_id)
        return jsonify(payload), code
    if request.method == "PUT":
        payload, code = update_wishlist_item(wishlist_id, item_id)
        return jsonify(payload), code
    payload, code = delete_wishlist_item(wishlist_id, item_id)
    return payload, code
