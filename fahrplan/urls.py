from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'fahrplan.views.index', name='home'),
    url(r'^login$', 'fahrplan.views.user_login', name='login'),
    url(r'^logout$', 'fahrplan.views.user_logout', name='logout'),
    url(r'autocomplete', 'fahrplan.views.autocomplete', name='autocomplete')
)
