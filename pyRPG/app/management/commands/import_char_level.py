import os
import glob
import json
import app.models as models
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import datetime as dt
import pyRPG.settings as settings

class Command(BaseCommand):
    help = ''

    @staticmethod
    def level_file():
        home_dir = os.path.join(settings.BASE_DIR, 'files/JSON/character_classes')
        level_class = glob.glob(os.path.join(home_dir, '*.json'))
        print(level_class)
        return level_class

    @staticmethod
    def class_level(index, lvl):
        for feat in lvl['levels']:
            try:
                if feat['rage'] != 'NaN':
                    rage = feat['rage']
            except:
                rage = None
            try:
                if feat['rageDamage'] != 'NaN':
                    rage_dmg = feat['rageDamage']
            except:
                rage_dmg = None
            try:
                if feat['cantrips'] != 'NaN':
                    cantrips = feat['cantrips']
            except:
                cantrips = None
            try:
                if feat['spells'] != 'NaN':
                    spells = feat['spells']
            except:
                spells = None
            try:
                if feat['martial_art'] != 'NaN':
                    martial_art = feat['martial_art']
            except:
                martial_art = None
            try:
                if feat['ki_points'] != 'NaN':
                    ki_points = feat['ki_points']
            except:
                ki_points = None
            try:
                if feat['unarmored_mvm'] != 'NaN':
                    unarmored_mvm = feat['unarmored_mvm']
            except:
                unarmored_mvm = None
            try:
                if feat['sneak'] != 'NaN':
                    sneak = feat['sneak']
            except:
                sneak = None
            try:
                if feat['sorcery_points'] != 'NaN':
                    sorcery_points = feat['sorcery_points']
            except:
                sorcery_points = None
            try:
                if feat['invocations'] != 'NaN':
                    invocations = feat['invocations']
            except:
                invocations = None
            try:
                if feat['spell_slots'] != 'NaN':
                    spell_slots = feat['spell_slots']
            except:
                spell_slots = None
            print(rage, rage_dmg, cantrips, spells, martial_art, ki_points, unarmored_mvm, sneak, sorcery_points, invocations, spell_slots)

    def handle(self, *args, **options):
        start_time = dt.datetime.now()
        class_lvl = self.level_file()

        print('--------Start--------')
        for index, f in enumerate(class_lvl):
            print(f)
            df = json.load(open(f, 'r'))
            self.class_level(index, df)
            print(dt.datetime.now() - start_time)
        print('--------End----------')
