# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-24 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_extraction', '0012_remove_rssdata_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssdata',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rssdata',
            name='death_no',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rssdata',
            name='header',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='rssdata',
            name='injury_no',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='rssdata',
            name='link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
