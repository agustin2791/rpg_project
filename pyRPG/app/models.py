from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    friends_list = models.ManyToManyField(User,
                                          related_name='user_friend_list')
    friend_request = models.ManyToManyField(User,
                                            related_name='user_request_list')

# Category for Items in the game
class ItemCategory(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(max_length=450)

    def __unicode__(self):
        return self.name

# Item Characteristics, can be equiped or stored in inventory
class Item(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(ItemCategory,
                                 related_name='item_category')
    lvl_req = models.IntegerField(default=1)
    class_exclusive = models.CharField(max_length=150,
                                       default='All')
    dextirity = models.IntegerField(null=True,
                                     blank=True)
    damage = models.IntegerField(null=True,
                                  blank=True)
    defence = models.IntegerField(null=True,
                                   blank=True)
    weight = models.FloatField(default=1.0)

    def __unicode__(self):
        return self.name

# Character class e.g. Heavy, Archer, Scientist etc.
class CharacterClass(models.Model):
    name = models.CharField(max_length=150)
    # hp = models.IntegerField(default=100)
    # full_hp = models.IntegerField(default=100)
    # damage = models.IntegerField(default=5)
    # speed = models.IntegerField(default=5)
    # defence = models.IntegerField(default=5)
    # dexterity = models.IntegerField(default=5)
    # constitution = models.IntegerField(default=5)
    # intelligence = models.IntegerField(default=5)
    # charisma = models.IntegerField(default=5)
    # wisdom = models.IntegerField(default=5)
    # inventory_limit = models.FloatField(default=50.0)
    enemy = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class CharacterRace(CharacterClass):
    def __unicode__(self):
        return self.name

# Character's attack
class Attack(models.Model):
    ATTACK_TYPE = (
        ('PRIMARY', 'PRIMARY'),
        ('SECONDARY', 'SECONDARY')
    )
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=100,
                            choices=ATTACK_TYPE)
    sub = models.BooleanField(default=False)
    enemy = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

# User's Character and Characteristics
class Character(models.Model):
    name = models.CharField(max_length=150)
    level = models.IntegerField(default=1)
    hp = models.IntegerField(default=100)
    full_hp = models.IntegerField(default=100)
    damage = models.IntegerField(default=5)
    speed = models.IntegerField(default=5)
    defence = models.IntegerField(default=5)
    dexterity = models.IntegerField(default=5)
    constitution = models.IntegerField(default=5)
    intelligence = models.IntegerField(default=5)
    charisma = models.IntegerField(default=5)
    wisdom = models.IntegerField(default=5)
    inventory = models.ManyToManyField(Item,
                                       related_name='char_inventory')
    inventory_limit = models.FloatField(default=50.0)
    exp = models.IntegerField(default=0)
    initiation = models.IntegerField(default=0)
    attack = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(User,
                             related_name='user_character')
    attack_type = models.ForeignKey(Attack,
                                    related_name='attack_type',
                                    blank=True,
                                    null=True)
    sub_attack_type = models.ForeignKey(Attack,
                                        related_name='sub_attack_type',
                                        blank=True,
                                        null=True)
    enemy = models.BooleanField(default=False)
    enemy_type = models.CharField(max_length=150,
                                  blank=True,
                                  null=True)
    gold = models.IntegerField(default=0)
    alignment = models.CharField(max_length=150,
                                 null=True,
                                 blank=True)
    hit_dice = models.CharField(max_length=100,
                                null=True,
                                blank=True)
    background = models.CharField(max_length=100,
                                  null=True,
                                  blank=True)


    def __unicode__(self):
        return self.name

    def get_campaign(self):
        campaigns = Campaign.objects.filter(characters__id=self.id)
        try:
            return campaigns[0]
        except IndexError:
            return None

class CharacterSkills(models.Model):
    character = models.ForeignKey(Character,
                                  on_delete=models.CASCADE,
                                  related_name='character_skills')
    acrobatics = models.IntegerField(default=0)
    anima_hand = models.IntegerField(default=0)
    arcana = models.IntegerField(default=0)
    athletics = models.IntegerField(default=0)
    deception = models.IntegerField(default=0)
    history = models.IntegerField(default=0)
    insight = models.IntegerField(default=0)
    intimidation = models.IntegerField(default=0)
    investigation = models.IntegerField(default=0)
    medicine = models.IntegerField(default=0)
    nature = models.IntegerField(default=0)
    perception = models.IntegerField(default=0)
    performance = models.IntegerField(default=0)
    persuasion = models.IntegerField(default=0)
    religion = models.IntegerField(default=0)
    soh = models.IntegerField(default=0)
    stealth = models.IntegerField(default=0)
    survival = models.IntegerField(default=0)


class CharacterFeature(models.Model):
    feature = models.CharField(max_length=150)
    description = models.TextField()
    character = models.ForeignKey(Character,
                                  on_delete=models.CASCADE,
                                  related_name='character_features')
    def __unicode__(self):
        return self.feature

class Campaign(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=300)
    host = models.ForeignKey(User,
                             related_name='campaign_host')
    player_limit = models.IntegerField(default=6)
    users = models.ManyToManyField(User,
                                   related_name='campaign_users')
    characters = models.ManyToManyField(Character,
                                       related_name='campaign_characters')
    chapters = models.ManyToManyField('CampaignChapter',
                                      related_name='campaign_chapters')
    objective = models.TextField()
    beginning = models.TextField()
    end = models.TextField()
    complete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def getEnemies(self):
        enemies = []
        for char in self.characters.all():
            if char.enemy:
                enemies.append(char)
        return enemies

class NonPlayableCharacters(models.Model):
    name = models.CharField(max_length=150)
    script = models.TextField()
    campaign = models.ForeignKey(Campaign,
                                 null=True,
                                 blank=True)

    def __unicode__(self):
        return self.name

class CampaignChapter(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=300)
    description = models.TextField()
    rooms = models.ManyToManyField('ChapterRoom')
    campaign = models.ForeignKey(Campaign,
                                 related_name='campaign')
    cleared = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class ChapterArea(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    number_of_rooms = models.IntegerField(default=3)
    cleared = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class ChapterRoom(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    npc = models.ManyToManyField(NonPlayableCharacters,
                                 related_name='room_npc')
    chapter_area = models.ForeignKey(ChapterArea,
                                     related_name='chapter_area')
    activity = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Battle(models.Model):
    name = models.CharField(max_length=150)
    enemies = models.ManyToManyField(Character,
                                     related_name='enemies')
    characters = models.ManyToManyField(Character,
                                        related_name='battle_character')
    number_of_commoner = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    description = models.TextField()
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)

    def __unicode__(self):
        return self.name
