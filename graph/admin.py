from django.contrib import admin

# Register your models here.
from .models import *
from news_extraction.models import *
#model admin options
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id","VehicleNo","Death","Injury","Year","Location",]
    #list_display_links = ["updated"]


    class Meta:
        model = News
admin.site.register(News, PostModelAdmin)

