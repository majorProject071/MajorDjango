from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = 'graph'

urlpatterns = [
    url(r'^ktm-map/$', views.index, name='index'),
    url(r'^location/$', views.location, name='location'),
    url(r'^searchnumber/$', views.searchnumber, name='search'),
]
