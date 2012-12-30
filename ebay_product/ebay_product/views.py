from django.http import HttpResponseRedirect, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import View, TemplateView

from ebay_product.forms import ActivateChargeForm, CreateChargeForm


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
                return HttpResponse("Installed")
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
