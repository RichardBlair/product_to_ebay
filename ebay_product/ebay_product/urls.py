from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from ebay_product import  views

urlpatterns = patterns('',
    url(r'^install/?$', login_required(views.InstallView.as_view()), name='install'),
    url(r'^ebay/?$', login_required(views.EbayAuthView.as_view()), name='ebay_auth'),
    url(r'^/?$', login_required(views.RootView.as_view()), name='root'),
    url(r'^shopify/', include('shopify.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls))
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
