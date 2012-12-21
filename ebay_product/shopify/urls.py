from django.conf.urls.defaults import patterns
from django.contrib.auth.decorators import login_required

from .views import ShopifyView, AuthView, AuthCallbackView, InstallView

NAMESPACE = {'namespace': 'shopify'}

urlpatterns = patterns(
    '',
    (r'^$', ShopifyView.as_view(), NAMESPACE, 'shopify.root'),
    (r'^auth/?$', AuthView.as_view(), NAMESPACE, 'shopify.auth'),
    (r'^auth_callback/?$', AuthCallbackView.as_view(), NAMESPACE,
        'shopify.auth_callback'),
    (r'^install/?$', login_required(InstallView.as_view()), NAMESPACE,
        'shopify.install')
)
