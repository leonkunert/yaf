from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'fahrplan.views.index', name='home'),
    url(r'login', 'fahrplan.views.login', name='login'),
    url(r'autocomplete', 'fahrplan.views.autocomplete', name='autocomplete')
)
