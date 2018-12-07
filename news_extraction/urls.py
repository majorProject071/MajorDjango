from django.conf.urls import url
from . import views

app_name = 'news_extraction'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'extraction$', views.extraction, name='extraction'),
    url(r'about_us', views.about_us, name='about_us'),
    url(r'contact_us', views.contact_us, name='contact_us'),
    url(r'search', views.searchquery, name='searchquery'),
]
