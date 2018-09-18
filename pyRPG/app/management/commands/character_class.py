import pandas as pd
import app.models as models
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import glob
import os
import datetime as dt
import pyRPG.settings as settings

class Command(BaseCommand):
    help = ''

    @staticmethod
    def character_file():
        char_file = glob.glob(os.path.join(settings.BASE_DIR, 'files/CSV/character_class.csv'))
        return char_file

    @staticmethod
    def character_class(index, row):
        equipment = []
        if row['Equip1'] != 'NaN':
            equipment.append(row['Equip1'])
        if row['Equip2'] != 'NaN':
            equipment.append(row['Equip2'])
        if row['Equip3'] != 'NaN':
            equipment.append(row['Equip3'])
        if row['Equip4'] != 'NaN':
            equipment.append(row['Equip4'])
        if row['EquipX'] != 'NaN':
            equipment.append(row['EquipX'])

        hp, hp_2 = row['HP'].split(', ')

        character = models.CharacterClass.objects.update_or_create(
            id=index,
            defaults={
                'name': row['Name'],
                'hit_dice': row['HitDice'],
                'hp': hp,
                'hp_2': hp_2,
                'saving_throws': row['SavingThrows'],
                'skills_limit': row['SkillsLimit'],
                'skills': row['Skills'],
            }
        )

        if len(equipment) > 0:
            for ind, equip in enumerate(equipment):
                new_id = int('{0}{1}'.format(index, ind))
                eq = models.CharacterClassEquipment.objects.update_or_create(
                    id=new_id,
                    defaults={
                        'char_class': character[0],
                        'desc': equip
                    }
                )

    def handle(self, *args, **options):
        start_time = dt.datetime.now()
        char_file = 'D:/software/rpg_one/pyRPG/files/CSV/character_class.csv'
        print char_file
        df = pd.read_csv(char_file, encoding='latin-1')
        print '----------Start---------'
        for index, row in enumerate(df.iterrows()):
            self.character_class(index, row[1])
            print (dt.datetime.now() - start_time)
        print '---------End------------'
