# Generated by Django 2.1.7 on 2019-03-31 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('level', models.IntegerField(default=1)),
                ('hp', models.IntegerField(default=100)),
                ('full_hp', models.IntegerField(default=100)),
                ('armor_class', models.IntegerField(default=5)),
                ('strength', models.IntegerField(default=5)),
                ('dexterity', models.IntegerField(default=5)),
                ('constitution', models.IntegerField(default=5)),
                ('intelligence', models.IntegerField(default=5)),
                ('charisma', models.IntegerField(default=5)),
                ('wisdom', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='EnemyAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='character',
            name='armor_class',
        ),
        migrations.RemoveField(
            model_name='character',
            name='charisma',
        ),
        migrations.RemoveField(
            model_name='character',
            name='constitution',
        ),
        migrations.RemoveField(
            model_name='character',
            name='dexterity',
        ),
        migrations.RemoveField(
            model_name='character',
            name='enemy',
        ),
        migrations.RemoveField(
            model_name='character',
            name='enemy_attack',
        ),
        migrations.RemoveField(
            model_name='character',
            name='enemy_damage',
        ),
        migrations.RemoveField(
            model_name='character',
            name='enemy_defence',
        ),
        migrations.RemoveField(
            model_name='character',
            name='enemy_type',
        ),
        migrations.RemoveField(
            model_name='character',
            name='full_hp',
        ),
        migrations.RemoveField(
            model_name='character',
            name='hp',
        ),
        migrations.RemoveField(
            model_name='character',
            name='id',
        ),
        migrations.RemoveField(
            model_name='character',
            name='intelligence',
        ),
        migrations.RemoveField(
            model_name='character',
            name='level',
        ),
        migrations.RemoveField(
            model_name='character',
            name='name',
        ),
        migrations.RemoveField(
            model_name='character',
            name='strength',
        ),
        migrations.RemoveField(
            model_name='character',
            name='wisdom',
        ),
        migrations.CreateModel(
            name='Enemy',
            fields=[
                ('basecharacter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.BaseCharacter')),
            ],
            bases=('app.basecharacter',),
        ),
        migrations.AddField(
            model_name='character',
            name='basecharacter_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.BaseCharacter'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enemyaction',
            name='enemy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Enemy'),
        ),
        migrations.AddField(
            model_name='enemy',
            name='actions',
            field=models.ManyToManyField(related_name='enemy_actions', to='app.EnemyAction'),
        ),
        migrations.AddField(
            model_name='enemy',
            name='attacks',
            field=models.ManyToManyField(related_name='enemy_attacks', to='app.EnemyAction'),
        ),
    ]
