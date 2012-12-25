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
    """
    Class that uses the API_ENDPOINTS to dynamically create methods
    for accessing the shopify API.
    """

    def __init__(self, access_token=None, shop=None):
        self.access_token = access_token
        self.shop = shop

    def __getattr__(self, name):
        """
        This method will try to find 'name' in the API_ENDPOINT dictionary and
        return a dynamic request method that will make accessing the API possible.

        Params:
            name - The name of the method or attribute that we will either
                    raise an error for or create a request method for.

        Returns:
            A request method which will be used to call the desired endpoint.

        Raises:
            AttributeError - When name is not in the dictionary
        """
        try:
            api_method = API_ENDPOINTS[name]
            return self._make_request(api_method['endpoint'] % self.shop,
                    api_method['method'])
        except KeyError:
            raise AttributeError("'Shoppy' object has no attribute '%s'" % name)

    def _make_request(self, url, method):
        """
        Method that encloses the request method.

        Params:
            url - The url enpoint that you are trying to hit
            method - the method used with the endpoint (get or post)

        Returns:
            A request method which has access to the url and method.
        """
        def request(**kwargs):
            """
            The method that takes data and params and makes the request to
            shopify.

            Params:
                params - The querystring parameters that you wish to add to the
                            request.
                data - When making a post request, data needs to be specified.

            Returns:
                The response in the form of a dictionary
            """
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
