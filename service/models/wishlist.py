"""
Wishlist data model
"""

import logging
from .persistent_base import (
    db,
    PersistentBase,
    DataValidationError,
    parse_timestamp,
    timestamp_column,
)

logger = logging.getLogger("flask.app")


class Wishlist(db.Model, PersistentBase):
    """
    Class that represents a Wishlist
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(63), nullable=True)
    is_private = db.Column(db.Boolean, nullable=False, default=False)
    created_at = timestamp_column()
    updated_at = timestamp_column()

    # one wishlist can contain many items
    items = db.relationship(
        "Item",
        backref="wishlist",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy=True,
    )

    def __repr__(self):
        return f"<Wishlist {self.name} id=[{self.id}]>"

    def serialize(self):
        """Serializes a Wishlist into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "customer_id": self.customer_id,
            "description": self.description,
            "is_private": self.is_private,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "items": [item.serialize() for item in self.items],
        }

    def deserialize(self, data):
        """
        Deserializes a Wishlist from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.customer_id = data["customer_id"]
            self.description = data.get("description")
            if "is_private" in data:
                raw_private = data["is_private"]
                if not isinstance(raw_private, bool):
                    raise DataValidationError(
                        "Invalid Wishlist: is_private must be a boolean"
                    )
                self.is_private = raw_private
            else:
                self.is_private = False
            created_at = data.get("created_at")
            updated_at = data.get("updated_at")
            self.created_at = parse_timestamp(created_at)
            self.updated_at = parse_timestamp(updated_at)
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Wishlist: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained bad or no data "
                + str(error)
            ) from error
        except ValueError as error:
            raise DataValidationError(
                "Invalid Wishlist: invalid datetime format"
            ) from error
        return self

    @classmethod
    def find_by_name(cls, name):
        """Returns all Wishlists with the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_customer_id(cls, customer_id):
        """Returns all Wishlists for the given customer_id"""
        logger.info("Processing customer_id query for %s ...", customer_id)
        return cls.query.filter(cls.customer_id == customer_id)

    @classmethod
    def find_by_description(cls, description):
        """Returns all Wishlists with the given description"""
        logger.info("Processing description query for %s ...", description)
        return cls.query.filter(cls.description == description)
