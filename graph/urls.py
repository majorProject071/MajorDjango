from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = 'graph'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^districts/$', views.districts, name='districts'),
    url(r'^bar/(?P<id>\d+)/$', views.yeargraph, name='yeargraph'),
    url(r'^bar/$', views.bar, name='bar'),
    url(r'^line/$', views.line, name='line'),
]
