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
        json_files = glob.glob(os.path.join(home_dir, '*.json'))
        return json_files

    @staticmethod
    def get_category_slug(cat):
        category_slug = cat.lower().split(' ')
        category_slug = '-'.join(category_slug)
        category = models.ItemCategory.objects.get_or_create(
            name=cat,
            defaults={
                'slug': category_slug
            }
        )[0]
        return category
    @staticmethod
    def import_ag(self, ag):
        for ad in ag:
            for a in ag[ad]:
                category = self.get_category_slug(a['category'])
                models.Item.objects.update_or_create(
                    name=a['item'],
                    defaults={
                        'category': category,
                        'cost': a['cost'],
                        'weight': a['weight'],
                        'container_cap': a['capacity'],
                        'description': a['description']
                    }
                )

    @staticmethod
    def import_armor(self, armor):
        for a in armor:
            for ar in armor[a]:
                category = self.get_category_slug(ar['category'])
                models.Item.objects.update_or_create(
                    name=ar['item'],
                    defaults={
                        'category': category,
                        'cost': ar['cost'],
                        'armor_class': ar['ac'],
                        'strength': ar['strength'],
                        'stealth': ar['stealth'],
                        'weight': ar['weight'],
                        'description': ar['description']
                    }
                )

    @staticmethod
    def import_mounts(self, mount):
        for mo in mount:
            for m in mount[mo]:
                category = self.get_category_slug(m['category'])
                models.Item.objects.update_or_create(
                    name=m['item'],
                    defaults={
                        'category': category,
                        'cost': m['cost'],
                        'speed': m['speed'],
                        'carry_cap': m['carry_cap'],
                        'weight': m['weight'],
                        'description': m['description']
                    }
                )

    @staticmethod
    def import_tools(self, tools):
        for tool in tools:
            for t in tools[tool]:
                category = self.get_category_slug(t['category'])
                models.Item.objects.update_or_create(
                    name=t['item'],
                    defaults={
                        'category': category,
                        'cost': t['cost'],
                        'weight': t['weight'],
                        'description': t['description']
                    }
                )

    @staticmethod
    def import_tg(self, trade_goods):
        for trade in trade_goods:
            for t in trade_goods[trade]:
                category = self.get_category_slug(t['category'])
                models.Item.objects.update_or_create(
                    name=t['item'],
                    defaults={
                        'category': category,
                        'cost': t['cost']
                    }
                )

    @staticmethod
    def import_weapons(self, weapons):
        for weapon in weapons:
            for w in weapons[weapon]:
                category = self.get_category_slug(w['category'])
                models.Item.objects.update_or_create(
                    name=w['item'],
                    defaults={
                        'category': category,
                        'cost': w['cost'],
                        'damage': w['damage'],
                        'weight': w['weight'],
                        'description': w['properties']
                    }
                )


    def handle(self, *args, **options):
        start_time = dt.datetime.now()
        json_files = self.get_json_files()

        print '-------Start-------'
        for f in json_files:
            data = json.load(open(f, 'r'))
            if 'adventure_gear' in data:
                print 'Adventure Gear >>>>'
                self.import_ag(self, data)
                print (dt.datetime.now() - start_time)
            elif 'light_armor' in data:
                print 'Armor >>>>>>'
                self.import_armor(self, data)
                print (dt.datetime.now() - start_time)
            elif 'mounts' in data:
                print 'Mounts >>>>>>>'
                self.import_mounts(self, data)
                print (dt.datetime.now() - start_time)
            elif 'trade_goods' in data:
                print 'Trade Goods >>>>>>'
                self.import_tg(self, data)
                print (dt.datetime.now() - start_time)
            elif 'simple_melee_weapons' in data:
                print 'Weapons >>>>>>>'
                self.import_weapons(self, data)
                print (dt.datetime.now() - start_time)


        print '--------End--------'
