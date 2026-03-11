"""
Item data model associated with a Wishlist
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


class Item(db.Model, PersistentBase):
    """Class that represents an Item belonging to a Wishlist"""

    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(
        db.Integer,
        db.ForeignKey("wishlist.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = db.Column(db.String(64), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    variant_id = db.Column(db.String(64), nullable=False)
    added_at = timestamp_column()
    updated_at = timestamp_column()

    def __repr__(self):
        return (
            f"<Item {self.product_name} id=[{self.id}] "
            f"wishlist_id=[{self.wishlist_id}]>"
        )

    def serialize(self):
        """Converts an Item into a dictionary"""
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "variant_id": self.variant_id,
            "added_at": self.added_at.isoformat() if self.added_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def deserialize(self, data):
        """Populates an Item from a dictionary"""
        try:
            self.wishlist_id = data["wishlist_id"]
            self.product_id = data["product_id"]
            self.product_name = data["product_name"]
            self.quantity = data.get("quantity", 1)
            self.variant_id = data["variant_id"]

            added_at = data.get("added_at")
            updated_at = data.get("updated_at")
            self.added_at = parse_timestamp(added_at)
            self.updated_at = parse_timestamp(updated_at)
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError("Invalid Item: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Item: body of request contained bad or no data " + str(error)
            ) from error
        except ValueError as error:
            raise DataValidationError("Invalid Item: invalid datetime format") from error

        return self

    @classmethod
    def find_by_wishlist_product_variant(cls, wishlist_id, product_id, variant_id):
        """Returns an Item matching the (wishlist_id, product_id, variant_id) combination"""
        logger.info(
            "Checking for duplicate: wishlist=%s product=%s variant=%s",
            wishlist_id, product_id, variant_id,
        )
        return cls.query.filter(
            cls.wishlist_id == wishlist_id,
            cls.product_id == product_id,
            cls.variant_id == variant_id,
        ).first()
