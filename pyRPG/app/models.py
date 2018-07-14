from django.db import models
from django.contrib.auth.models import User

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
    dextirity = models.IntergerField(null=True,
                                     blank=True)
    damage = models.IntergerField(null=True,
                                  blank=True)
    defence = models.IntergerField(null=True,
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
    defence = models.IntergerField(null=True,
                                   blank=True)
    luck = models.IntergerField(null=True,
                                blank=True)
    barter = models.IntergerField(null=True,
                                  blank=True)
    perception = models.IntergerField(null=True,
                                      blank=True)

    def __unicode__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=150)
    character_class = models.ForeignKey(CharacterClass)
    hp = models.IntergerField(default=100)
    damage = models.IntergerField(default=10)
    defence = models.IntergerField(default=10)
    luck = models.IntergerField(default=10)
    barter = models.IntergerField(default=10)
    perception = models.IntergerField(default=10)
    inventory = modes.ManyToManyField(Item)
    inventory_limit = models.FloatField(default=50.0)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def add_class(self, *args, **kwargs):
        cClass = CharacterClass.objects.get(id=self.character_class.id)
        self.hp += cClass.health
        self.damage += cClass.damage
        self.defence += cClass.defence
        self.luck += cClass.luck
        self.barter += cClass.barter
        self.perception += cClass.perception
        super(Character, self).save(*args, **kwargs)
