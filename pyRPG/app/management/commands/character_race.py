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
    def load_characters():
        home_dir = os.path.join(settings.BASE_DIR, 'file/JSON/character_race')
        characters = glob.glob(os.path.join(home_dir, '*.json'))

        return characters

    @staticmethod
    def character(index, char):
        if char['sub_class'] != None:
            sub_class = True
        else:
            sub_class = False

        character = models.CharacterRace.objects.update_or_create(
            id=index,
            defaults={
                'name': char['name'],
                'desc': char['description'],
                'ability_score_increase': char['ability_score_increase'],
                'age': char['age'],
                'alignment': char['alignment'],
                'size': char['size'],
                'speed': char['speed'],
                'language': char['language'],
                'sub_race': False
            }
        )
        if char['additional_traits'] != None:
            for ind, trait in enumerate(char['additional_traits']):
                char_traits = models.CharacterRaceTraits.objects.update_or_create(
                    id=ind,
                    defaults={
                        'char_race': character[0],
                        'trait': trait['name'],
                        'desc': trait['description']
                    }
                )

        if sub_class:
            sub_character = models.CharacterRace.objects.update_or_create(
                id=index,
                defaults={
                    'name': char['sub_class']['name'],
                    'desc': char['sub_class']['description'],
                    'ability_score_increase': char['sub_class']['ability_score_increase'],
                    'age': char['age'],
                    'alignment': char['alignment'],
                    'size': char['size'],
                    'speed': char['speed'],
                    'language': char['language'],
                    'sub_race': sub_class
                }
            )
            for ind, trait in enumerate(char['additional_traits']):
                char_traits = models.CharacterRaceTraits.objects.update_or_create(
                    id=ind,
                    defaults={
                        'char_race': sub_character[0],
                        'trait': trait['name'],
                        'desc': trait['description']
                    }
                )
            for ind, trait in enumerate(char['sub_class']['additional_traits']):
                char_traits = models.CharacterRaceTraits.objects.update_or_create(
                    id=ind,
                    defaults={
                        'char_race': sub_character[0],
                        'trait': trait['name'],
                        'desc': trait['description']
                    }
                )

    def handle(self, *args, **options):
        characters = self.load_characters()
        start_time = dt.datetime.now()

        print '---------- Start ---------'
        for index, c in enumerate(characters):
            data = json.load(open(c, 'r'))
            self.character(index, data)
            print(dt.datetime.now() - start_time)

        print '---------- End -----------'
