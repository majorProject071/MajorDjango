# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-07-23 05:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='rssdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(blank=True, max_length=200)),
                ('body', models.TextField()),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('death', models.CharField(blank=True, max_length=100, null=True)),
                ('death_no', models.IntegerField(blank=True, default=0, null=True)),
                ('injury', models.CharField(blank=True, max_length=100, null=True)),
                ('injury_no', models.IntegerField(blank=True, default=0, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicleone', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicletwo', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.CharField(blank=True, default=datetime.date.today, max_length=100, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('vehicle_no', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_type', models.CharField(blank=True, max_length=100, null=True)),
                ('month', models.CharField(blank=True, max_length=100, null=True)),
                ('season', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.CharField(blank=True, max_length=100, null=True)),
                ('day', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-date', 'location', 'vehicleone', 'vehicletwo'),
                'verbose_name': 'rssdata',
            },
        ),
    ]
