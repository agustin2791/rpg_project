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
    health = models.IntegerField(null=True,
                                 blank=True)
    damage = models.IntegerField(null=True,
                                 blank=True)
    defence = models.IntegerField(null=True,
                                   blank=True)
    luck = models.IntegerField(null=True,
                                blank=True)
    barter = models.IntegerField(null=True,
                                  blank=True)
    perception = models.IntegerField(null=True,
                                      blank=True)

    def __unicode__(self):
        return self.name

class CharacterRace(CharacterClass):
    def __unicode__(self):
        return self.name

# Character's attack
class CharacterAttack(models.Model):
    ATTACK_TYPE = (
        ('PRIMARY', 'PRIMARY'),
        ('SECONDARY', 'SECONDARY')
    )
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=100,
                            choices=ATTACK_TYPE)

    def __unicode__(self):
        return self.name

# User's Character and Characteristics
class Character(models.Model):
    name = models.CharField(max_length=150)
    level = models.IntegerField(default=1)
    character_class = models.ForeignKey(CharacterClass,
                                        related_name='character_class')
    character_race = models.ForeignKey(CharacterRace,
                                       related_name='character_race')
    hp = models.IntegerField(default=100)
    damage = models.IntegerField(default=10)
    defence = models.IntegerField(default=10)
    luck = models.IntegerField(default=10)
    barter = models.IntegerField(default=10)
    perception = models.IntegerField(default=10)
    inventory = models.ManyToManyField(Item,
                                       related_name='char_inventory')
    inventory_limit = models.FloatField(default=50.0)
    exp = models.IntegerField(default=0)
    initiation = models.IntegerField(default=0)
    attack = models.IntegerField()
    user = models.ForeignKey(User,
                             related_name='user_character')

    def __unicode__(self):
        return self.name

    def add_class(self, *args, **kwargs):
        cClass = CharacterClass.objects.get(id=self.character_class.id)
        cRace = CharacterRace.objects.get(id=self.character_race.id)
        self.hp += cClass.health + cRace.health
        self.damage += cClass.damage + cRace.damage
        self.defence += cClass.defence + cRace.defence
        self.luck += cClass.luck + cRace.luck
        self.barter += cClass.barter + cRace.barter
        self.perception += cClass.perception + cRace.perception
        super(Character, self).save(*args, **kwargs)

# minion, boss, mini boss
class EnemyCategory(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name

class EnemyAttack(models.Model):
    name = models.CharField(max_length=150)
    multiple = models.BooleanField(default=False)
    single = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Enemy(models.Model):
    name = models.CharField(max_length=150)
    health = models.IntegerField()
    damage = models.IntegerField()
    defence = models.IntegerField()
    initiation = models.IntegerField(default=0)
    attack = models.ForeignKey(EnemyAttack,
                               related_name='primary_attack')
    subAttack = models.ForeignKey(EnemyAttack,
                                  related_name='secondary_attack')

    def __unicode__(self):
        return self.name

class NonPlayableCharacters(models.Model):
    name = models.CharField(max_length=150)
    script = models.TextField()

    def __unicode__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=300)
    host = models.ForeignKey(User,
                             related_name='campaign_host')
    player_limit = models.IntegerField(default=6)
    users = models.ManyToManyField(User,
                                   related_name='campaign_users')
    chracters = models.ManyToManyField(Character,
                                       related_name='campaign_characters')
    chapters = models.ManyToManyField('CampaignChapter',
                                      related_name='campaign_chapters')
    objective = models.TextField()
    beginning = models.TextField()
    end = models.TextField()
    complete = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class CampaignEnemies(models.Model):
    name = models.CharField(max_length=150)
    health = models.IntegerField()
    damage = models.IntegerField()
    defence = models.IntegerField()
    initiation = models.IntegerField(default=0)
    attack = models.ForeignKey(EnemyAttack,
                               related_name='primary_enemy_attack')
    subAttack = models.ForeignKey(EnemyAttack,
                                  related_name='secondary_enemy_attack')
    campaign = models.ForeignKey(Campaign)

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
    enemies = models.ManyToManyField(CampaignEnemies,
                                     related_name='room_enemies')
    chapter_area = models.ForeignKey(ChapterArea,
                                     related_name='chapter_area')
    activity = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
