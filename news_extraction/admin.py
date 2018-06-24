# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","link","header","source","body","death","death_no","injury","injury_no","location","vehicle_involved","date","created_at","updated_at",]

    #list_display_links = ["updated"]


    class Meta:
        model = rssdata
admin.site.register(rssdata, PostModelAdmin)

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","post","vehicle_no","vehicle_type"]


    #list_display_links = ["updated"]


    class Meta:
        model = Vehicledetail
admin.site.register(Vehicledetail, PostModelAdmin)

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","post","day","month","season","year"]


    #list_display_links = ["updated"]


    class Meta:
        model = Datedetail
admin.site.register(Datedetail, PostModelAdmin)