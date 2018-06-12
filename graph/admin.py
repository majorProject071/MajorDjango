from django.contrib import admin

# Register your models here.
from .models import *
#model admin options
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","VehicleNo","Death","Injury","Year","Location",]
    #list_display_links = ["updated"]


    class Meta:
        model = News
admin.site.register(News, PostModelAdmin)

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","header","body","death","death_no","injury","injury_no","location","vehicle_involved","vehicle_no","date","day","created_at","updated_at",]

    #list_display_links = ["updated"]


    class Meta:
        model = rssdata
admin.site.register(rssdata, PostModelAdmin)