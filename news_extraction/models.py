from datetime import date

from django.db import models

class rssdata(models.Model):
    header = models.CharField(blank=True, max_length=100)
    body = models.TextField(blank=False, null=False)
    death = models.CharField(blank=True, max_length=100, null=True)
    death_no = models.IntegerField(blank=True, null=True)
    injury = models.CharField(blank=True, max_length=100, null=True)
    injury_no = models.IntegerField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=100, null=True)
    vehicle_no = models.CharField(blank=True, max_length=100, null=True)
    date = models.DateField(default=date.today, blank=True, null=True)
    day = models.CharField(blank=True, max_length=100, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'rssdata'
        ordering = ('-date', 'location')

    def save(self, *args, **kwargs):
        super(rssdata, self).save(*args, **kwargs)

    def __str__(self):
        return self.header