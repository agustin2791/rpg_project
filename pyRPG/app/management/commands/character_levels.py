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
    def get_file():
        file = glob.glob(os.path.join(settings.BASE_DIR, 'files\CSV\character_levels.csv'))
        return file

    @staticmethod
    def character_level(row):
        character = models.CharacterClass.objects.get(id=int(row['Class ID']), name=row['Class'])
        if row['Rage'] == 'none':
            rage = None
        else:
            rage = int(row['Rage'])

        if row['Rage Damage'] == 'none':
            rage_dmg = None
        else:
            rage_dmg = int(row['Rage Damage'])

        if row['Cantrips Known'] == 'none':
            cantrip = None
        else:
            cantrip = int(row['Cantrips Known'])

        if row['Spells Known'] == 'none':
            spells = None
        else:
            spells = int(row['Spells Known'])

        if row['Martial Art'] == 'none':
            martial_art = None
        else:
            martial_art = row['Martial Art']

        if row['Ki Points'] == 'none':
            ki_points = None
        else:
            ki_points = int(row['Ki Points'])

        if row['Unarmored MVMT'] == 'none':
            unarmored_mvm = None
        else:
            unarmored_mvm = int(row['Unarmored MVMT'])

        if row['Sneak'] == 'none':
            sneak = None
        else:
            sneak = row['Sneak']

        if row['Sorc Points'] == 'none':
            sorcery_points = None
        else:
            sorcery_points = int(row['Sorc Points'])

        if row['Spell Slots'] == 'none':
            spell_slot = None
        else:
            spell_slot = int(row['Spell Slots'])

        if row['Slot Level'] == 'none':
            slot_level = None
        else:
            slot_level = int(row['Slot Level'])

        if row['Invocations'] == 'none':
            invocations = None
        else:
            invocations = int(row['Invocations'])

        if row['Slot 1'] == 'none':
            spell_slots_1 = 0
        else:
            spell_slots_1 = int(row['Slot 1'])

        if row['Slot 2'] == 'none':
            spell_slots_2 = 0
        else:
            spell_slots_2 = int(row['Slot 2'])

        if row['Slot 3'] == 'none':
            spell_slots_3 = 0
        else:
            spell_slots_3 = int(row['Slot 3'])

        if row['Slot 4'] == 'none':
            spell_slots_4 = 0
        else:
            spell_slots_4 = int(row['Slot 4'])

        if row['Slot 5'] == 'none':
            spell_slots_5 = 0
        else:
            spell_slots_5 = int(row['Slot 5'])

        if row['Slot 6'] == 'none':
            spell_slots_6 = 0
        else:
            spell_slots_6 = int(row['Slot 6'])

        if row['Slot 7'] == 'none':
            spell_slots_7 = 0
        else:
            spell_slots_7 = int(row['Slot 7'])

        if row['Slot 8'] == 'none':
            spell_slots_8 = 0
        else:
            spell_slots_8 = int(row['Slot 8'])

        if row['Slot 9'] == 'none':
            spell_slots_9 = 0
        else:
            spell_slots_9 = int(row['Slot 9'])

        level = models.CharacterClassLevel.objects.update_or_create(
            id=int(row['Index']),
            defaults={
                'char_class': character,
                'level': row['Level'],
                'pro_bonus': int(row['Proficiency Bonus']),
                'rage': rage,
                'rage_dmg': rage_dmg,
                'cantrips': cantrip,
                'spells': spells,
                'martial_art': martial_art,
                'ki_points': ki_points,
                'unarmored_mvm': unarmored_mvm,
                'sneak': sneak,
                'sorcery_points': sorcery_points,
                'spell_slot': spell_slot,
                'slot_level': slot_level,
                'invocations': invocations,
                'spell_slots_1': spell_slots_1,
                'spell_slots_2': spell_slots_2,
                'spell_slots_3': spell_slots_3,
                'spell_slots_4': spell_slots_4,
                'spell_slots_5': spell_slots_5,
                'spell_slots_6': spell_slots_6,
                'spell_slots_7': spell_slots_7,
                'spell_slots_8': spell_slots_8,
                'spell_slots_9': spell_slots_9,
            }
        )[0]
        level.save()

    def handle(self, *args, **options):
        start_time = dt.datetime.now()
        file = self.get_file()[0]
        print(file)
        df = pd.read_csv(file, encoding='latin-1')
        print ('---------Start---------')
        for row in df.iterrows():
            self.character_level(row[1])
            print (dt.datetime.now() - start_time)
        print('---------End------------')
