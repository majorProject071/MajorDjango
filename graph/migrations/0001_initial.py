# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-28 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VehicleNo', models.CharField(max_length=120)),
                ('Death', models.IntegerField(default=None)),
                ('Injury', models.IntegerField(default=None)),
                ('Year', models.IntegerField(default=None)),
                ('Location', models.CharField(default=None, max_length=120)),
            ],
        ),
    ]
