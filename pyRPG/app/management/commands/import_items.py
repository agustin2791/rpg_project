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
    def get_json_files():
        home_dir = os.path.join(settings.BASE_DIR, 'files/JSON/items')
        json_files = glob.glob(os.path.join(home_dir, 'armor.json'))
        return json_files

    @staticmethod
    def import_ag(data):
        pass

    def import_armor(index, data):
        print index
        for la in data['light_armor']:
            print la['item']

    def handle(self, *args, **options):
        start_time = dt.datetime.now()
        json_files = self.get_json_files()

        for f in json_files:
            data = json.load(open(f, 'r'))
            if 'light_armor' in data:
                self.import_armor(data)

        print (dt.datetime.now() - start_time)
        print '--------End--------'
