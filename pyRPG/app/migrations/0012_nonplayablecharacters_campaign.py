# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-13 05:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20180811_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonplayablecharacters',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Campaign'),
        ),
    ]