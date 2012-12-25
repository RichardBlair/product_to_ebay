#TODO: Remove dependancy on django
from django.utils import simplejson

import requests

API_ENDPOINTS = {
            'createRecurringCharge': {
                    'method': 'post',
                    'endpoint': 'https://%s/admin/recurring_application_charges.json'
                },
            'getRecurringCharge': {
                    'method': 'get',
                    'endpoint': 'https://%s/admin/recurring_application_charges/%(id)s.json'
                },
            'getRecurringCharges': {
                    'method': 'get',
                    'endpoint': 'https://%s/admin/recurring_application_charges.json'
                },
            'getProducts': {
                    'method': 'get',
                    'endpoint': 'https://%s/admin/products.json'
                },
        }


class Shoppy(object):

    def __init__(self, access_token=None, shop=None):
        self.access_token = access_token
        self.shop = shop

    def __getattr__(self, name):
        try:
            api_method = API_ENDPOINTS[name]
            return self._make_request(api_method['endpoint'] % self.shop,
                    api_method['method'])
        except KeyError:
            raise AttributeError("'Shoppy' object has no attribute '%s'" % name)

    def _make_request(self, url, method):
        def request(**kwargs):
            headers = {
                    'X-Shopify-Access-Token': self.access_token
                }

            if method == 'get':
                resp = requests.get(url, headers=headers,
                        params=kwargs.get('params'))
            elif method == 'post':
                resp = request.post(url, headers=headers,
                        data=kwargs.get('data'), params=kwargs.get('params'))

            return simplejson.loads(resp.content)

        return request
