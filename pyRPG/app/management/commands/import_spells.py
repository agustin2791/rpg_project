import pandas as pd
import app.models as models
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import glob
import os
import datetime as dt

class Command(BaseCommand):
    help = ''

    @staticmethod
    def get_data_file():
        '''
        This will get the spells and import them to the DB
        '''
        spell_file = glob.glob(os.path.join('/home/rpg_csv', 'spells.csv'))
        return (spell_file)

    @staticmethod
    def add_new_spell(row):
        # spell_level = row['Spell level']
        try:
            spell_level = row['Spell_level']
            if isinstance(spell_level, basestring) or not isinstance(spell_level, numbers.Number):
                spell_level = 0
        except:
            spell_level = 0
        print 'Spell LEVEL:',spell_level
        spell_ritual = row['Ritual']
        if spell_ritual == 'Ritual':
            spell_ritual = True
        else:
            spell_ritual = False

        models.Spells.objects.update_or_create(
                id=row['ID'],
                defaults={
                        'level': spell_level,
                        'spell_name': row['Spell_Name'],
                        'time': row['Casting_Time'],
                        'rang': row['Range'],
                        'comp': row['Components'],
                        'duration': row['Duration'],
                        'school': row['School'],
                        'ritual': spell_ritual,
                        'material': row['Material_Component'],
                        'description': row['Description'],

                    }
            )[0]

    def handle(self, *args, **options):
        starttime = dt.datetime.now()

        spell_file = self.get_data_file()
        today = dt.date.today().strftime('%Y%m%d')

        for f in spell_file:
            if f:
                print f
                print '--------START----------'
                df = pd.read_csv(f, encoding='latin-1')
                for row in df.iterrows():
                    print row[1]
                    self.add_new_spell(row[1])
                    print(dt.datetime.now() - starttime)

                print '--------END----------'
