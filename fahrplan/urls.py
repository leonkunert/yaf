from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'fahrplan.views.fahrplan'),
    url(r'^logout$', 'fahrplan.views.user_logout'),
    url(r'^login$', 'fahrplan.views.user_login'),
    url(r'^userStatus$', 'fahrplan.views.user_status'),
    url(r'^haltestellen$', 'fahrplan.views.getHaltestellen'),
    # else:
    url(r'^.*$', 'fahrplan.views.fahrplan')
)
