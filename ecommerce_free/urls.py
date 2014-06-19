# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ecommerce_free.core.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
