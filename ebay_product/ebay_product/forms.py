from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

from shopify.api import Shoppy

from ebay_product.models import ApplicationCharge


class ShopForm(forms.Form):

    def __init__(self, shop, **kwargs):
        super(ShopForm, self).__init__(**kwargs)
        self.shop = shop
        self.shoppy = Shoppy(access_token=self.shop.access_token,
                shop=self.shop.myshopify_domain)


class ActivateChargeForm(ShopForm):
    charge_id = forms.IntegerField(required=True)

    def clean_charge_id(self):
        try:
            self.charge = ApplicationCharge.objects.get(shop=self.shop,
                    charge_id=self.cleaned_data['charge_id'])
        except ApplicationCharge.DoesNotExist:
            raise forms.ValidationError('Charge does not exist')

        return self.cleaned_data['charge_id']

    def save(self, commit=True):
        self.shoppy.activateRecurringCharge(id=self.charge.charge_id)
        self.charge.status = 1
        if commit:
            self.charge.save()

        return self.charge


class CreateChargeForm(ShopForm):
    charge_name = forms.CharField(max_length=150)
    charge_price = forms.FloatField()

    def save(self, commit=True):
        charge = {
                    'recurring_application_charge': {
                            'name': self.cleaned_data['charge_name'],
                            'price': self.cleaned_data['charge_price'],
                            'test': True,
                            'return_url': '%s%s' % (settings.DOMAIN,
                                reverse('install'))
                        }
                }

        resp = self.shoppy.createRecurringCharge(data=charge)

        #This could raise a key error, and im not catching it on purpose.
        #If a person is having a problem signing up I want it to be very loud.
        app_charge = ApplicationCharge(shop=self.shop,
            price=charge['recurring_application_charge']['price'],
            name=charge['recurring_application_charge']['name'],
            charge_id=resp['recurring_application_charge']['id'])

        if commit:
            app_charge.save()

        return resp
