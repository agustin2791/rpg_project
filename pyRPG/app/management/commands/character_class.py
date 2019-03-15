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
        )[0]
        armor = row['Armor']
        character.armor.clear()
        # if ', ' in armor: print 'Yes'
        if armor != 'none':
            if armor and ', ' in armor:
                armor = armor.split(', ')
                for a in armor:
                    if a == 'Shields':
                        ar = models.ItemCategory.objects.get(name='Shield')
                        character.armor.add(ar)
                    elif a == 'All armor':
                        ar = models.ItemCategory.objects.filter(name__contains='Armor')
                        for i in ar: character.armor.add(i)
                    else:
                        ar = models.ItemCategory.objects.get(name=a)
                        character.armor.add(ar)
                    character.save()
            else:
                if 'All armor' in armor:
                    ar = models.ItemCategory.objects.filter(name__contains='Armor')
                    character.armor.add(ar)
                    for i in ar: character.armor.add(i)
                else:
                    ar = models.ItemCategory.objects.get(name=armor)
                    character.armor.add(ar)

        weapons = row['Weapons']
        if ', ' in weapons:
            weapons = weapons.split(', ')
            for w in weapons:
                w = w.title()
                if w == 'Simple Weapons' or w == 'Martial Weapons':
                    if w == 'Simple Weapons':
                        weapons_category = models.ItemCategory.objects.filter(name__contains='Simple')
                    if w == 'Martial Weapons':
                        weapons_category = models.ItemCategory.objects.filter(name__contains=w)
                    for c in weapons_category: character.weapons.add(c)
                else:
                    if 'Crossbow' in w:
                        a, b = w.split(' ')
                        cross = [b, a]
                        w = ', '.join(cross)
                    weapon_item = models.Item.objects.get(name=w)
                    character.weapon_items.add(weapon_item)
        else:
            if weapons == 'Simple weapons':
                weapons_category = models.ItemCategory.objects.filter(name__contains='Simple')
            for c in weapons_category: character.weapons.add(c)

        tools = row['Tools']
        try:
            tools = tools.title()
            tool_item = models.Item.objects.get(name=tools)
            character.tools_item.add(tool_item)
        except:
            pass

        if len(equipment) > 0:
            for ind, equip in enumerate(equipment):
                new_id = int('{0}{1}'.format(index, ind))
                eq = models.CharacterClassEquipment.objects.update_or_create(
                    id=new_id,
                    defaults={
                        'char_class': character,
                        'desc': equip
                    }
                )

    def handle(self, *args, **options):
        start_time = dt.datetime.now()
        char_file = 'D:/software/rpg_one/pyRPG/files/CSV/character_class.csv'
        print(char_file)
        df = pd.read_csv(char_file, encoding='latin-1')
        print('----------Start---------')
        for index, row in enumerate(df.iterrows()):
            self.character_class(index, row[1])
            print (dt.datetime.now() - start_time)
        print('---------End------------')
