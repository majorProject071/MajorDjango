from django.conf import settings
from django.db import models

#image table
class News(models.Model):
    VehicleNo = models.CharField(max_length=120)
    Death = models.CharField(max_length=120, default=0)
    Injury = models.CharField(max_length=120, default=0)
    Year = models.CharField(max_length=120,default=None)
    Location = models.CharField(max_length=120, default=None)
