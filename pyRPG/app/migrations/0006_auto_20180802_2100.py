# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-03 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180730_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='barter',
        ),
        migrations.RemoveField(
            model_name='character',
            name='luck',
        ),
        migrations.RemoveField(
            model_name='character',
            name='perception',
        ),
        migrations.AddField(
            model_name='character',
            name='charisma',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='character',
            name='constitution',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='character',
            name='dexterity',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='character',
            name='intelligence',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='character',
            name='speed',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='character',
            name='wisdom',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='character',
            name='damage',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='character',
            name='defence',
            field=models.IntegerField(default=5),
        ),
    ]
