"""
Test Factory to make fake objects for testing
"""

from datetime import timezone
from factory import Factory, Sequence, Faker
from service.models import Wishlist, Item


class WishlistFactory(Factory):
    """Creates fake Wishlists"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Persistent class"""

        model = Wishlist

    id = Sequence(lambda n: n)
    name = Faker("word")
    customer_id = Sequence(lambda n: n + 1000)
    description = Faker("sentence", nb_words=4)
    is_private = False
    created_at = Faker("date_time", tzinfo=timezone.utc)
    updated_at = Faker("date_time", tzinfo=timezone.utc)


class ItemFactory(Factory):
    """Creates fake Items"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Persistent class"""

        model = Item

    id = Sequence(lambda n: n)
    wishlist_id = Sequence(lambda n: n + 1)
    product_id = Sequence(lambda n: f"SKU-{n:05d}")
    product_name = Faker("word")
    quantity = Faker("random_int", min=1, max=5)
    variant_id = Sequence(lambda n: f"VAR-{n:05d}")
    added_at = Faker("date_time", tzinfo=timezone.utc)
    updated_at = Faker("date_time", tzinfo=timezone.utc)
