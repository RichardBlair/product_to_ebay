from django.http import HttpResponseRedirect, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.conf import settings

from ebaysuds import EbaySuds
import redis

from shopify.api import Shoppy

from ebay_product.forms import ActivateChargeForm, CreateChargeForm
from ebay_product.models import EbaySettings


class InstallView(View):
    """
    View to handle creating a charge and activating a charge.
    """

    def get(self, request, *args, **kwargs):
        try:
            form_data = {'charge_id': request.GET['charge_id']}
            activate_form = ActivateChargeForm(request.user, data=form_data)

            if activate_form.is_valid():
                activate_form.save()
                return HttpResponseRedirect(reverse('root'))
        except (MultiValueDictKeyError):
            pass

        charge_data = {
                    'charge_name': 'eBay List',
                    'charge_price': 4.99
                }

        create_charge = CreateChargeForm(request.user, data=charge_data)
        if create_charge.is_valid():
            charge_resp = create_charge.save()
            return HttpResponseRedirect(charge_resp['recurring_application_charge']['confirmation_url'])


class EbayAuthView(View):
    """View that will handle the eBay auth call back and get the auth token"""

    def get(self, request, *args, **kwargs):
        try:
            ebay_settings = EbaySettings.objects.get(shop=self.request.user)
        except EbaySettings.DoesNotExist:
            return HttpResponseRedirect(reverse('root'))

        ebay = EbaySuds(token=None, sandbox=True, app_id=settings.EBAY_APP_ID,
                site_id=settings.EBAY_SITE_ID, dev_id=settings.EBAY_DEV_ID,
                cert_id=settings.EBAY_CERT_ID)

        token = ebay.FetchToken(SessionID=ebay_settings.session_id)
        ebay_settings.token = token.eBayAuthToken
        ebay_settings.token_expires = token.HardExpirationTime
        ebay_settings.save()

        return HttpResponseRedirect(reverse('root'))


class RootView(TemplateView):
    """
    Display products that can be published and ask for ebay auth if we do not
    yet have ebay info.
    """

    template_name = 'root.html'

    def get_context_data(self, **kwargs):
        try:
            ebay_settings = EbaySettings.objects.get(shop=self.request.user)
        except EbaySettings.DoesNotExist:
            ebay_settings = EbaySettings(shop=self.request.user)

        if ebay_settings.token is None:
            ebay = EbaySuds(token=None, sandbox=True, app_id=settings.EBAY_APP_ID,
                    site_id=settings.EBAY_SITE_ID, dev_id=settings.EBAY_DEV_ID,
                    cert_id=settings.EBAY_CERT_ID)
            ebay_settings.session_id = ebay.GetSessionID(RuName=settings.EBAY_RU_NAME).SessionID
            ebay_settings.save()

        return {
                'ebay_settings': ebay_settings,
                'ebay_ru_name': settings.EBAY_RU_NAME,
                'shopify_products': products
            }


def get_products(shop):
    redis_con = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
            db=settings.REDIS_DB)

    products = redis_con.get('%s:products' % shop.myshopify_domain)
    if products is None:
        shoppy = Shoppy(access_token=shop.access_token,
                shop=shop.myshopify_domain)
        products = shoppy.getProducts(params={'limit': 250})
        #Make the cache expire after 24 hours
        redis_con.setex('%s:products' % shop.myshopify_domain, products, (24 * 60 * 60))

    return products
