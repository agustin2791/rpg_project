# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-20 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180919_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='damage',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]