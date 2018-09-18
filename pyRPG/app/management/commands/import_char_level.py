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
        level_class = glob.glob(os.path.join(os.path.join(settings.BASE_DIR, 'file/JSON/character_classes'), '*.json'))
        return level_class

    @staticmethod
    def class_level(index, lvl):
        for feat in level['levels']:
            if lvl['rage'] != 'NaN':
                rage = lvl['rage']
            else:
                rage = None
            if lvl['rage_dmg'] != 'NaN':
                rage_dmg = lvl['rage_dmg']
            else:
                rage = None
            if lvl['cantrips'] != 'NaN':
                cantrips = lvl['cantrips']
            else:
                cantrips = None
            if lvl['spells'] != 'NaN':
                spells = lvl['spells']
            else:
                spells = None
            if lvl['martial_art'] != 'NaN':
                martial_art = lvl['martial_art']
            else:
                martial_art = None
            if lvl['ki_points'] != 'NaN':
                ki_points = lvl['ki_points']
            else:
                ki_points = None
            if lvl['unarmored_mvm'] != 'NaN':
                unarmored_mvm = lvl['unarmored_mvm']
            else:
                unarmored_mvm = None
            if lvl['sneak'] != 'NaN':
                sneak = lvl['sneak']
            else:
                sneak = None
            if lvl['sorcery_points'] != 'NaN':
                sorcery_points = lvl['sorcery_points']
            else:
                sorcery_points = None
            if lvl['invocations'] != 'NaN':
                invocations = lvl['invocations']
            else:
                invocations = None
            if lvl['spell_slots'] != 'NaN':
                spell_slots = lvl['spell_slots']
            else:
                spell_slots = None
