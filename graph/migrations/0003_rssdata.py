# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-12 11:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0002_auto_20180528_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='rssdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(blank=True, max_length=100)),
                ('body', models.TextField()),
                ('death', models.CharField(blank=True, max_length=100, null=True)),
                ('death_no', models.IntegerField(blank=True, null=True)),
                ('injury', models.CharField(blank=True, max_length=100, null=True)),
                ('injury_no', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_involved', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_no', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('day', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
