# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import rssdata

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","link","header","body","death","death_no","injury","injury_no","location","vehicle_involved","vehicle_no","date","day","month","season","year","created_at","updated_at",]

    #list_display_links = ["updated"]


    class Meta:
        model = rssdata
admin.site.register(rssdata, PostModelAdmin)