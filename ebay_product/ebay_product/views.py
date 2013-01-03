from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.conf import settings

from ebaysuds import EbaySuds

from shopify.api import Shoppy
from shopify.models import Shop

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


class RootView(TemplateView):
    template_name = 'root.html'

    def get_context_data(self, **kwargs):
        try:
            ebay_settings = EbaySettings.objects.get(shop=self.request.user)
            ebay_sessionid = None
        except EbaySettings.DoesNotExist:
            ebay_settings = None
            ebay = EbaySuds(token=None, sandbox=True, app_id=settings.EBAY_APP_ID,
                    site_id=settings.EBAY_SITE_ID, dev_id=settings.EBAY_DEV_ID,
                    cert_id=settings.EBAY_CERT_ID)
            ebay_sessionid = ebay.GetSessionID(RuName=settings.EBAY_RU_NAME)

        return {
                'ebay_settings': ebay_settings,
                'ebay_sessionid': ebay_sessionid,
                'ebay_ru_name': settings.EBAY_RU_NAME
            }
