from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.utils import simplejson

from shopify.api import Shoppy


class InstallView(View):

    def get(self, request, *args, **kwargs):
        shop = Shoppy(access_token=request.user.access_token,
                shop=request.user.myshopify_domain)
        resp = shop.getProducts(some_param='param')
        return HttpResponse(simplejson.dumps(resp))
