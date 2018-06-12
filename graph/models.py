from django.conf import settings
from django.db import models
from datetime import date

#image table
class News(models.Model):
    VehicleNo = models.CharField(max_length=120)
    Death = models.CharField(max_length=120, default=0)
    Injury = models.CharField(max_length=120, default=0)
    Year = models.CharField(max_length=120,default=None)
    Location = models.CharField(max_length=120, default=None)

class rssdata(models.Model):
    header = models.CharField(blank=True, max_length=100)
    body = models.TextField(blank=False, null=False)
    death = models.CharField(blank=True, max_length=100, null=True)
    death_no = models.IntegerField(blank=True, null=True)
    injury = models.CharField(blank=True, max_length=100, null=True)
    injury_no = models.IntegerField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=100, null=True)
    vehicle_involved = models.CharField(blank=True, max_length=100, null=True)
    vehicle_no = models.CharField(blank=True, max_length=100, null=True)
    date = models.DateField(default=date.today, blank=True, null=True)
    day = models.CharField(blank=True, max_length=100, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)