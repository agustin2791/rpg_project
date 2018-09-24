# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-22 02:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_item_container_cap'),
    ]

    operations = [
        migrations.RenameField(
            model_name='character',
            old_name='defence',
            new_name='armor_class',
        ),
        migrations.RenameField(
            model_name='character',
            old_name='damage',
            new_name='strength',
        ),
        migrations.RemoveField(
            model_name='character',
            name='attack',
        ),
        migrations.RemoveField(
            model_name='character',
            name='attack_type',
        ),
        migrations.RemoveField(
            model_name='character',
            name='sub_attack_type',
        ),
        migrations.AlterField(
            model_name='character',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
