"""
Models for Wishlist service

All of the models are stored in this package
"""

from .persistent_base import db, DataValidationError
from .wishlist import Wishlist
from .item import Item
