from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.urlresolvers import reverse
from django.views.generic import View, TemplateView
from django.conf import settings

from shopify.api import Shoppy

from .models import ApplicationCharge


class InstallView(View):
    """
    View to handle creating a charge and activating a charge.

    TODO:
        Move the logic into a form.
    """

    def get(self, request, *args, **kwargs):
        shop = Shoppy(access_token=request.user.access_token,
                shop=request.user.myshopify_domain)

        try:
            charge = ApplicationCharge.objects.get(shop=request.user,
                    charge_id=request.GET['charge_id'])
            shop.activateRecurringCharge(id=charge.charge_id)
            charge.status = 1
            charge.save()
        except (ApplicationCharge.DoesNotExist, MultiValueDictKeyError):
            charge = {
                        'recurring_application_charge': {
                                'name': 'eBay lister',
                                'price': 4.99,
                                'test': True,
                                'return_url': '%s%s' % (settings.DOMAIN,
                                    reverse('install'))
                            }
                    }
            resp = shop.createRecurringCharge(data=charge)

            #This could raise a key error, and im not catching it on purpose.
            #If a person is having a problem signing up I want it to be very loud.
            ApplicationCharge.objects.create(shop=request.user,
                    price=charge['recurring_application_charge']['price'],
                    name=charge['recurring_application_charge']['name'],
                    charge_id=resp['recurring_application_charge']['id']
                    )
            return HttpResponseRedirect(resp['recurring_application_charge']['confirmation_url'])
