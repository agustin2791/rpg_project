# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-03 06:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20180802_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CharacterSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acrobatics', models.IntegerField(default=0)),
                ('anima_hand', models.IntegerField(default=0)),
                ('arcana', models.IntegerField(default=0)),
                ('athletics', models.IntegerField(default=0)),
                ('deception', models.IntegerField(default=0)),
                ('history', models.IntegerField(default=0)),
                ('insight', models.IntegerField(default=0)),
                ('intimidation', models.IntegerField(default=0)),
                ('investigation', models.IntegerField(default=0)),
                ('medicine', models.IntegerField(default=0)),
                ('nature', models.IntegerField(default=0)),
                ('perception', models.IntegerField(default=0)),
                ('performance', models.IntegerField(default=0)),
                ('persuasion', models.IntegerField(default=0)),
                ('religion', models.IntegerField(default=0)),
                ('soh', models.IntegerField(default=0)),
                ('stealth', models.IntegerField(default=0)),
                ('survival', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='character',
            name='character_class',
        ),
        migrations.RemoveField(
            model_name='character',
            name='character_race',
        ),
        migrations.RemoveField(
            model_name='characterclass',
            name='barter',
        ),
        migrations.RemoveField(
            model_name='characterclass',
            name='damage',
        ),
        migrations.RemoveField(
            model_name='characterclass',
            name='defence',
        ),
        migrations.RemoveField(
            model_name='characterclass',
            name='health',
        ),
        migrations.RemoveField(
            model_name='characterclass',
            name='luck',
        ),
        migrations.RemoveField(
            model_name='characterclass',
            name='perception',
        ),
        migrations.AddField(
            model_name='character',
            name='description',
            field=models.TextField(default='Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='character',
            name='full_hp',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='character',
            name='enemy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='characterskills',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_skills', to='app.Character'),
        ),
        migrations.AddField(
            model_name='characterfeature',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_features', to='app.Character'),
        ),
    ]
