import urllib

import requests

from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import (Http404, HttpResponseForbidden, HttpResponseRedirect,
                            HttpResponse)
from django.conf import settings
from django.utils import simplejson

from .models import Shop
from .api import ShopifyRequest


class ShopifyMixin(object):
    """
    This class makes shopify convience methods easily available anywhere.
    """

    def request_is_valid(self, request, code):
        """
        Simple method to deal with checking is a request from shopify
        is valid.
        """
        req = ShopifyRequest(settings.SHOPIFY_SHARED_SECRET)
        return req.is_valid(request.GET['shop'], code, request.GET['timestamp'],
                request.GET['signature'])

    def authenticate_request(self, request, code=None):
        shop = authenticate(shop=request.GET['shop'], code=code,
                timestamp=request.GET['timestamp'], signature=request.GET['signature'])
        return shop


class ShopifyView(View, ShopifyMixin):
    """
    This is the main entry point for shopify apps. This endpoint should
    always have a shop querystring parameter passed to it.

    Based of the shop querystring paramet we will either:
        a) Redirect to the core app if the shop exists on system
        b) Begin the install process

    Required:
        request.get must have a shop in the dictionary
    """

    def get(self, request, *args, **kwargs):
        if 'shop' not in request.GET:
            raise Http404

        try:
            #Will throw an exception is the object does not exist
            #forcing a redirect to the oauth process
            shop = Shop.objects.get(myshopify_domain=request.GET['shop'])

            #This checks to see that shopify is the result of this request
            #Because shopify is the only one that knows the shared secret
            #this is works as our login.
            shop = self.authenticate_request(request)
            if shop is None:
                return HttpResponseForbidden()

            login(request, shop)

            #If there is an account, redirect to the core app
            return HttpResponseRedirect('/')
        #If the shop is not in the databse, go through the install process
        except Shop.DoesNotExist:
            url_params = {'shop': request.GET['shop']}
            redirect_url = '%s/?%s' % (reverse('shopify.auth'),
                    urllib.urlencode(url_params))
            return HttpResponseRedirect(redirect_url)


class AuthView(View, ShopifyMixin):
    """
    This endpoint will begin the process of requesting an oauth token from
    shopify.

    Required:
        request.get must have a shop in the dictionary
    """

    def get(self, request, *args, **kwargs):
        if 'shop' not in request.GET:
            raise Http404

        #The permissions we will ask the shop owner for
        permissions = ['read_products', 'write_products']

        #build a dictionary of query string parameters
        url_params = {
                        'scope': ','.join(permissions),
                        'client_id': settings.SHOPIFY_API_KEY,
                        'redirect_uri': '%s%s' % (settings.DOMAIN,
                            reverse('shopify.auth_callback'))
                }

        #encode query string parameters with the oauth endpoint
        url = 'https://%(shop)s/admin/oauth/authorize?%(params)s' % {
                    'shop': request.GET['shop'],
                    'params': urllib.urlencode(url_params)
                }

        return HttpResponseRedirect(url)


class AuthCallbackView(View, ShopifyMixin):
    """
    This is the auth call back. Ideally shopify will redict back to us
    with a temporary token. With this temporary token we will get a real
    access token and save it.

    Required:
        request.get must have a shop in the dictionary
    """

    def get(self, request, *args, **kwargs):
        if 'shop' not in request.GET:
            raise Http404

        parameters = {
                    'code': request.GET['code'],
                    'client_id': settings.SHOPIFY_API_KEY,
                    'client_secret': settings.SHOPIFY_SHARED_SECRET
                }

        resp = requests.post('https://%s/admin/oauth/access_token' % request.GET['shop'],
            params=parameters)

        token = simplejson.loads(resp.content)
        try:
            #At this point we must be sure that the request are coming from shopify
            if not self.request_is_valid(request, request.GET['code']):
                return HttpResponseForbidden()

            shop = Shop.objects.create(myshopify_domain=request.GET['shop'],
                access_token=token['access_token'], code=request.GET['code'])

            shop = self.authenticate_request(request, request.GET['code'])
            if shop is None:
                return HttpResponseForbidden()
            login(request, shop)

            return HttpResponseRedirect(reverse('install'))
        except KeyError:
            return HttpResponseForbidden()
