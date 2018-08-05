from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = 'graph'

urlpatterns = [
    url(r'^ktm-map/$', views.index, name='kathmandu'),
    url(r'^location/$', views.bargraph, name='location'),
    url(r'^searchnumber/$', views.searchnumber, name='search'),
    url(r'^nepal-map/$', views.nepalmap, name='nepal'),
    url(r'^linegraph/$', views.linegraph, name='linegraph'),
]
