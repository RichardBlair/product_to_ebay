from django.conf.urls.defaults import patterns

from .views import ShopifyView, AuthView, AuthCallbackView

NAMESPACE = {'namespace': 'shopify'}

urlpatterns = patterns(
    '',
    (r'^$', ShopifyView.as_view(), NAMESPACE, 'shopify.root'),
    (r'^auth/?$', AuthView.as_view(), NAMESPACE, 'shopify.auth'),
    (r'^auth_callback/?$', AuthCallbackView.as_view(), NAMESPACE, 'shopify.auth_callback')

)
