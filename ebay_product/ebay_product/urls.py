from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ebay_product.views.home', name='home'),
    # url(r'^ebay_product/', include('ebay_product.foo.urls')),
    url(r'^shopify/', include('shopify.urls')),


    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls))
)
