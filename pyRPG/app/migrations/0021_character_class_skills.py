# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-01 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_character_bg_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='class_skills',
            field=models.IntegerField(default=0),
        ),
    ]
