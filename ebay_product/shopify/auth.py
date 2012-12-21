from django.conf import settings

from .api import ShopifyRequest
from .models import Shop


class ShopBackend(object):

    def authenticate(self, shop=None, code=None, timestamp=None, signature=None):
        """
        Authenticate a shop based off the information sent in the request
        sent from shopify, and the shared secret.

        Params:
            shop: The my shopify domain for the shop
            code: The code sent by shopify
            timestamp: The timestamp sent by shopify
            signature: The signature sent by shopify

        Returns:
            A shop if everything is okay, none otherwise
        """
        req = ShopifyRequest(settings.SHOPIFY_SHARED_SECRET)
        if req.is_valid(shop, code, timestamp, signature):
            try:
                return Shop.objects.get(myshopify_domain=shop)
            except Shop.DoesNotExist:
                return None
        else:
            return None

    def get_user(self, user_id):
        """
        Return a shop given it's user id.

        Returns:
            The shop, or none
        """
        try:
            return Shop.objects.get(id=user_id)
        except Shop.DoesNotExist:
            return None
