from django.conf.urls import url
from . import views

app_name = 'news_extraction'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'extraction$', views.extraction, name='extraction'),
]

