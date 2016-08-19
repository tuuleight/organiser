# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-17 16:54
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactive_calendar', '0003_auto_20160816_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attenders',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='event',
            name='invited',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), default=list, size=None),
        ),
    ]
