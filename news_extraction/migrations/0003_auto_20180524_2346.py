# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-24 18:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_extraction', '0002_auto_20180524_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rssdata',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
