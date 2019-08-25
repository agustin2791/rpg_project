import os
from django.db import models
from django.contrib.auth.models import User
import app.views as views

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends_list = models.ManyToManyField(User,
                                          related_name='user_friend_list')
    friend_request = models.ManyToManyField(User,
                                            related_name='user_request_list')

# Category for Items in the game
class ItemCategory(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(max_length=450)

    def __str__(self):
        return self.name

# Item Characteristics, can be equiped or stored in inventory
class Item(models.Model):
    name = models.CharField(max_length=150)
    # melee weapon, light armor etc.
    category = models.ForeignKey(ItemCategory,
                                 related_name='item_category',
                                 on_delete=models.PROTECT)
    cost = models.CharField(max_length=100)
    armor_class = models.CharField(max_length=120,
                                      blank=True,
                                      null=True)
    strength = models.IntegerField(null=True,
                                   blank=True)
    stealth = models.CharField(max_length=50,
                               blank=True,
                               null=True)
    speed = models.IntegerField(null=True,
                               blank=True)
    carry_cap = models.IntegerField(null=True,
                                    blank=True)
    container_cap = models.CharField(max_length=100,
                                     null=True,
                                     blank=True)
    damage = models.CharField(max_length=100,
                              null=True,
                                  blank=True)
    weight = models.FloatField(default=1.0,
                               null=True,
                               blank=True)
    description = models.TextField(null=True,
                                   blank=True)

    def __str__(self):
        return self.name

# Spells for characters
class Spells(models.Model):
    level = models.IntegerField(default=0)
    spell_name = models.CharField(max_length=150)
    time = models.CharField(max_length=50)
    rang = models.CharField(max_length=50)
    comp = models.CharField(max_length=150)
    duration = models.CharField(max_length=150)
    school = models.CharField(max_length=150)
    ritual = models.BooleanField(default=False)
    material = models.CharField(max_length=200,
                                null=True,
                                blank=True)
    description = models.TextField()
    classes = models.ManyToManyField('CharacterClass')

    def __str__(self):
        return self.spell_name

# Character class e.g. Heavy, Archer, Scientist etc.
class CharacterClass(models.Model):
    name = models.CharField(max_length=150)
    hit_dice = models.CharField(max_length=200)
    hp = models.CharField(max_length=200)
    hp_2 = models.CharField(max_length=200)
    armor = models.ManyToManyField(ItemCategory,
                              related_name='armor_category')
    weapons = models.ManyToManyField(ItemCategory,
                                     related_name='weapons_category')
    weapon_items = models.ManyToManyField(Item,
                                          related_name='weapons_available')
    tools = models.ManyToManyField(ItemCategory,
                                   related_name='tools_category')
    tools_item = models.ManyToManyField(Item,
                                       related_name='tools_available')
    saving_throws = models.CharField(max_length=150)
    skills_limit = models.IntegerField(default=2)
    skills = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_armor(self):
        armor = self.armor.all()
        armor_list = []
        if armor:
            for a in armor:
                armor_list.append(a.name)
            armor_text = ' | '.join(armor_list)
        else:
            armor_text = 'No Armor Proficiencies'
        return armor_text

    def get_weapons(self):
        category = self.weapons.all()
        item = self.weapon_items.all()
        weapons_list = []
        if category:
            for c in category:
                weapons_list.append(c.name)
        if item:
            for i in item:
                weapons_list.append(i.name)
        return ' | '.join(weapons_list)

    def get_tools(self):
        tools_item = self.tools_item.all()
        tool_list = []
        if tools_item:
            for t in tools_item:
                tool_list.append(t.name)
            return ', '.join(tool_list)
        elif self.name == 'Bard':
            return 'Three musical instruments of your choice'
        elif self.name == 'Monk':
            return 'Choose one type of artisan\'s tools or one musical instrument'
        else:
            return 'None'
    
    def get_equipment(self):
        eq = CharacterClassEquipment.objects.filter(char_class=self.id).exclude(desc='nan')
        to_choose = []
        for e in eq:
            equipment = e.desc
            equipment = equipment.split(', ')
            to_choose.append(equipment)
        return to_choose

# Chracter class equipment
class CharacterClassEquipment(models.Model):
    char_class = models.ForeignKey(CharacterClass,
                                    on_delete=models.PROTECT)
    desc = models.CharField(max_length=150)

class CharacterClassLevel(models.Model):
    char_class = models.ForeignKey(CharacterClass,
                                   on_delete=models.CASCADE)
    level = models.IntegerField()
    pro_bonus = models.IntegerField()
    # Barbarian
    rage = models.IntegerField(null=True,
                               blank=True)
    rage_dmg = models.IntegerField(null=True,
                                   blank=True)
    # Bard, Cleric, Druid, Sorcerer, Wralock
    cantrips = models.IntegerField(null=True,
                                   blank=True)
    # Bard, Ranger, Sorcerer, Warlock, Wizard
    spells = models.IntegerField(null=True,
                                 blank=True)
    # Monk
    martial_art = models.CharField(max_length=10,
                                   null=True,
                                   blank=True)
    ki_points = models.IntegerField(null=True,
                                    blank=True)
    unarmored_mvm = models.IntegerField(null=True,
                                        blank=True)
    # Rogue
    sneak = models.CharField(max_length=10,
                             null=True,
                             blank=True)
    # Sorcerer
    sorcery_points = models.IntegerField(blank=True,
                                         null=True)
    # Warlock
    spell_slot = models.IntegerField(blank=True,
                                     null=True)
    slot_level = models.IntegerField(blank=True,
                                     null=True)
    invocations = models.IntegerField(blank=True,
                                      null=True)
    # Spell Slots
    spell_slots_1 = models.IntegerField(default=0)
    spell_slots_2 = models.IntegerField(default=0)
    spell_slots_3 = models.IntegerField(default=0)
    spell_slots_4 = models.IntegerField(default=0)
    spell_slots_5 = models.IntegerField(default=0)
    spell_slots_6 = models.IntegerField(default=0)
    spell_slots_7 = models.IntegerField(default=0)
    spell_slots_8 = models.IntegerField(default=0)
    spell_slots_9 = models.IntegerField(default=0)

    def get_level_features(self):
        features = CharacterClassFeature.objects.filter(char_class=self.id)

    def __str__(self):
        return '{0} at Level {1}'.format(self.char_class.name, self.level)

class CharacterClassFeature(models.Model):
    char_class = models.ForeignKey(CharacterClass,
                                   related_name='char_class_feature',
                                   on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    feature = models.CharField(max_length=150)
    description = models.TextField()

class CharacterRace(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    ability_score_increase = models.TextField()
    age = models.TextField()
    alignment = models.TextField()
    size = models.TextField()
    speed = models.TextField()
    language = models.TextField()
    sub_race = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def character_traits(self):
        return CharacterRaceTraits.objects.filter(char_race=self.id)

class CharacterRaceTraits(models.Model):
    char_race = models.ForeignKey(CharacterRace,
                                  related_name='character_race_trait',
                                  on_delete=models.CASCADE)
    trait = models.CharField(max_length=50)
    desc = models.TextField()

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

    def __str__(self):
        return self.name

# User's Character and Characteristics
def user_character_img(instance, filename):
    return '{0}/chracter/{1}'.format(instance.user.id, filename)

def user_character_thumb(instance, filename):
    return '{0}/chracter/thumb/{1}'.format(instance.user.id, filename)

class Character(models.Model):
    user = models.ForeignKey(User,
                             related_name='user_character',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    level = models.IntegerField(default=1)
    hp = models.IntegerField(default=100)
    full_hp = models.IntegerField(default=100)
    armor_class = models.IntegerField(default=5)
    strength = models.IntegerField(default=5)
    dexterity = models.IntegerField(default=5)
    constitution = models.IntegerField(default=5)
    intelligence = models.IntegerField(default=5)
    charisma = models.IntegerField(default=5)
    wisdom = models.IntegerField(default=5)
    speed = models.IntegerField(default=5)
    c_class = models.ForeignKey(CharacterClass,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False)
    c_race = models.ForeignKey(CharacterRace,
                                on_delete=models.CASCADE,
                                blank=False,
                                null=False)
    inventory = models.ManyToManyField(Item,
                                       related_name='char_inventory')
    inventory_limit = models.FloatField(default=50.0)
    exp = models.IntegerField(default=0)
    initiation = models.IntegerField(default=0)
    description = models.TextField(null=True,
                                   blank=True)
    gold = models.IntegerField(default=0)
    spells = models.ManyToManyField(Spells,
                                    blank=True,
                                    null=True)
    alignment = models.CharField(max_length=150,
                                 null=True,
                                 blank=True)
    hit_dice = models.CharField(max_length=100,
                                null=True,
                                blank=True)
    background = models.CharField(max_length=100,
                                  null=True,
                                  blank=True)
    background_skills = models.TextField(blank=True,
                                         null=True)
    saving_throws = models.CharField(max_length=150,
                                     null=True,
                                     blank=True)
    proficiency_bonus = models.IntegerField(default=2,
                                            null=True,
                                            blank=True)
    # Skill sets related to Class
    skill_set = models.CharField(max_length=100,
                                 blank=True,
                                 null=True)
    # Skill set limit related to background max 2
    bg_skills = models.IntegerField(default=0)
    class_skills = models.IntegerField(default=0)
    personality_traits = models.TextField(null=True,
                                          blank=True)
    ideals = models.TextField(null=True,
                              blank=True)
    bonds = models.TextField(null=True,
                             blank=True)
    flaws = models.TextField(null=True,
                             blank=True)
    equipment = models.TextField(null=True,
                                 blank=True)
    image = models.ImageField(upload_to=user_character_img,
                              null=True,
                              blank=True)
    thumbnail = models.ImageField(upload_to=user_character_thumb,
                                  null=True,
                                  blank=True)


    def __str__(self):
        return self.name

    # Get the campagin in which the character belongs to
    def get_campaign(self):
        campaigns = Campaign.objects.filter(characters__id=self.id)
        try:
            return campaigns[0]
        except IndexError:
            return None

    # Get the character's abilities
    def get_abilities(self):
        abilities = []
        # 
        ability = ['strength', 'dexterity', 'constitution', 'intelligence', 'charisma', 'wisdom']
        for a in ability:
            ab = Character.objects.values_list(a, flat=True).get(id=self.id)
            mod = views.get_modifier(ab)
            if mod > 0:
                mod = '+{0}'.format(mod)
            abilities.append([a.title(), ab, mod])
        return abilities
    # Get the character's alignment
    def get_alignment(self):
        al = self.alignment.split(': ') # split alignment text and return the name of alignment
        return al[0]

    # Get the character's information Personality traits, ideals etc...
    # The idea is more for templating ease
    def get_character_info(self):
        info = []
        # declare traits
        traits = ['Personality Traits', 'Ideals', 'Bonds', 'Flaws']
        for t in traits:
            # get the character's traits from model
            search = t.lower()
            search = '_'.join(search.split(' '))
            i = Character.objects.values_list(search, flat=True).get(id=self.id)
            # append the trait and their value
            info.append([search, t, i])

        return info

    # get the list of spells that is available for the character's class
    def get_spell_list(self):
        spells = Spells.objects.filter(level__lte=self.level, classes__id__in=[self.c_class.id]).order_by('level')
        levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        spell_levels = []

        for l in levels:
            if l <= self.level:
                spell_level = []
                for s in spells:
                    if s.level == l and s not in self.spells.all():
                        spell_level.append(s)
                spell_levels.append(spell_level)

        return spell_levels
    
    # def get_spell_slots():

    def skills_limit(self):
        if self.skill_set:
            skills = self.skill_set.split(', ')
            set_length = len(skills)
            limit = self.c_class.skills_limit + 2
            if set_length == limit:
                return False
            else:
                return True
        else:
            return True

    def skill_list(self):
        if self.skill_set:
            return self.skill_set.split(', ')

    def choose_class_skills(self):
        all_skills = views.SKILLS
        seclected_skills = []

        if self.c_class.skills == 'Any':
            return all_skills
        else:
            class_skill = self.c_class.skills.split(', ')
            for s in all_skills:
                if self.skill_set:
                    char_skills = self.skill_set.split(', ')
                    if s[1] in class_skill and s[0] not in char_skills:
                        seclected_skills.append([s[0], s[1]])
                else:
                    if s[1] in class_skill:
                        seclected_skills.append([s[0], s[1]])
            return seclected_skills

    def choose_bg_skills(self):
        all_skills = views.SKILLS
        seclected_skills = []
        if self.skill_set is not None:
            char_skills = self.skill_set.split(', ')
            for s in all_skills:
                if s[0] not in char_skills:
                    seclected_skills.append({s[0], s[1]})

            return seclected_skills
        else:
            return all_skills
    
    def saving_throws_list(self):
        c_class = self.c_class
        st = c_class.saving_throws.lower().split(', ')
        print(st)
        return st

    def get_saving_throws(self):
        abilities = []
        ability = ['strength', 'dexterity', 'constitution', 'intelligence', 'charisma', 'wisdom']
        st = self.saving_throws_list()
        for a in ability:
            ab = Character.objects.values_list(a, flat=True).get(id=self.id)
            if a in st:
                mod = views.get_modifier(ab) + self.proficiency_bonus
                style = 'border: solid 2px #16a085;'
            else:
                mod = views.get_modifier(ab)
                style = ''
            if mod > 0:
                mod = '+{0}'.format(mod)
            abilities.append([a.title(), ab, mod, style])
        return abilities

    def get_all_weapons(self):
        if self.inventory.count() > 0:
            inventory = self.inventory
            inv = []
            for i in inventory.all():
                inv.append(i.id)
            weapons = Item.objects.filter(category__name__contains='Weapons').exlcude(id__in=inv).order_by('name')
        else:
            weapons = Item.objects.filter(category__name__contains='Weapons').order_by('name')
        return weapons

    def choose_starting_equipment(self):
        eq = CharacterClassEquipment.objects.filter(char_class=self.c_class).exclude(desc='nan')
        equipment = []
        for e in eq:
            if ', ' in e.desc:
                opt = e.desc.split(', ')
                equipment.append(opt)
            else:
                equipment.append([e.desc])
        return equipment

    def character_class_spells(self):
        cl = CharacterClassLevel.objects.get(char_class=self.c_class, level=self.level)
        spell_slots = [cl.cantrips, cl.spell_slots_1, cl.spell_slots_2, cl.spell_slots_3, cl.spell_slots_4, cl.spell_slots_5, cl.spell_slots_6, cl.spell_slots_7, cl.spell_slots_8, cl.spell_slots_9]
        return spell_slots

    def get_armor_class(self):
        inventory = self.inventory.filter()
        armor = []
        if inventory:
            for i in inventory:
                if 'Armor' in i.category.name:
                    armor.append(i)
        ac = 0
        if armor:
            for a in armor:
                if ' + ' in a.armor_class:
                    ac = int(a.armor_class.split(' + ')[0])
                    if 'max ' in a.armor_class:
                        max_mod = int(a.armor_class.split(' ')[-1].replace(')', ''))
                        dex = views.get_modifier(self.dexterity)
                        if dex <= max_mod:
                            ac += dex
                        else:
                            ac += max_mod
                else:
                    ac += int(a.armor_class)
        if ac == 0:
            ac = 0
        return ac

    def get_currency(self):
        coin = CharacterCurrency.objects.get(character=self.id)
        return coin

    # def get_class_features(self):
    #     feats = CharacterClassFeature.objects.filter(char_class=self.c_class, level=self.level)
    #     return feats
class CharacterSkills(models.Model):
    character = models.OneToOneField(Character,
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

    def get_skills(self):
        skills = []
        names = views.SKILLS
        char_skills = self.character.skill_set
        if char_skills:
            pro_skills = char_skills.split(', ')
        else:
            pro_skills = False
        for n in sorted(names):
            mod = CharacterSkills.objects.values_list(n[0], flat=True).get(pk=self.id)
            if pro_skills:
                if n[0] in pro_skills:
                    mod += self.character.proficiency_bonus
            if mod > 0:
                mod = '+{0}'.format(mod)
            s = [n[1], mod, n[0]]
            skills.append(s)
        return skills

class CharacterCurrency(models.Model):
    character = models.ForeignKey(Character,
                                    related_name='character_currency',
                                    on_delete=models.CASCADE)
    copper = models.IntegerField(default=0)
    silver = models.IntegerField(default=0)
    electrum = models.IntegerField(default=0)
    gold = models.IntegerField(default=0)
    platinum = models.IntegerField(default=0)

    def __str__(self):
        return self.character.name


class CharacterBackground(models.Model):
    background = models.CharField(max_length=100)
    description = models.TextField(null=True,
                                   blank=True)
    character = models.ForeignKey(Character,
                                  on_delete=models.CASCADE,
                                  related_name='character_background')

    def __str__(self):
        return self.background

class CharacterFeature(models.Model):
    feature = models.CharField(max_length=150)
    description = models.TextField()
    character = models.ForeignKey(Character,
                                  on_delete=models.CASCADE,
                                  related_name='character_features')
    def __str__(self):
        return self.feature


'''
///////////////////////////
///////////////////////////
Campaign //////////////////
///////////////////////////
///////////////////////////
'''
class Campaign(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=300)
    host = models.ForeignKey(User,
                             related_name='campaign_host',
                             on_delete=models.CASCADE)
    player_limit = models.IntegerField(default=6)
    users = models.ManyToManyField(User,
                                   related_name='campaign_users')
    characters = models.ManyToManyField(Character,
                                       related_name='campaign_characters')
    chapters = models.ManyToManyField('CampaignChapter',
                                      related_name='campaign_chapters')
    enemies = models.ManyToManyField('Enemy',
                                    related_name='campaign_enemies')
    objective = models.TextField()
    beginning = models.TextField()
    end = models.TextField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def getEnemies(self):
        enemies = []
        for char in self.characters.all():
            if char.enemy:
                enemies.append(char)
        return enemies

class Enemy(models.Model):
    enemy_user = models.ForeignKey(User,
                             related_name='user_enemy',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    level = models.IntegerField(default=1)
    hp = models.IntegerField(default=100)
    full_hp = models.IntegerField(default=100)
    armor_class = models.IntegerField(default=5)
    strength = models.IntegerField(default=5)
    dexterity = models.IntegerField(default=5)
    constitution = models.IntegerField(default=5)
    intelligence = models.IntegerField(default=5)
    charisma = models.IntegerField(default=5)
    wisdom = models.IntegerField(default=5)
    speed = models.IntegerField(default=5)
    actions = models.ManyToManyField('EnemyAction', related_name='enemy_actions')
    info = models.ManyToManyField('EnemyAction', related_name='enemy_info')

class EnemyAction(models.Model):
    enemy = models.ForeignKey(Enemy,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()

class NonPlayableCharacters(models.Model):
    name = models.CharField(max_length=150)
    script = models.TextField()
    campaign = models.ForeignKey(Campaign,
                                 null=True,
                                 blank=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CampaignChapter(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=300)
    description = models.TextField()
    rooms = models.ManyToManyField('ChapterRoom')
    campaign = models.ForeignKey(Campaign,
                                 related_name='campaign',
                                 on_delete=models.CASCADE)
    cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# For Future
class ChapterArea(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    number_of_rooms = models.IntegerField(default=3)
    cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.name

#For Future
class ChapterRoom(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    npc = models.ManyToManyField(NonPlayableCharacters,
                                 related_name='room_npc')
    chapter_area = models.ForeignKey(ChapterArea,
                                     related_name='chapter_area',
                                     on_delete=models.CASCADE)
    activity = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Battle(models.Model):
    battle_enemies = models.ManyToManyField(Character,
                                     related_name='enemies')
    battle_characters = models.ManyToManyField(Character,
                                        related_name='battle_character')
    number_of_commoner = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    description = models.TextField()
    campaign = models.ForeignKey(Campaign,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True)

    def __str__(self):
        return self.name

class CampaignNote(models.Model):
    campaign = models.ForeignKey(Campaign,
                                    on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    note = models.TextField()

    def __str__(self):
        return self.title

class ChapterNote(models.Model):
    chapter = models.ForeignKey(CampaignChapter,
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    note = models.TextField()

    def __str__(self):
        return self.title

class Forum(models.Model):
    title = models.CharField(max_length=200)
    entry = models.TextField()
    post_by = models.ForeignKey(UserProfile,
                                on_delete=models.PROTECT)
    posted_on = models.DateField(auto_now=True)
    last_edit = models.DateField(auto_now_add=True)
    points = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

    def get_comments(self):
        comments = ForumComment.objects.filter(forum=self.id)


class ForumComment(models.Model):
    forum = models.ForeignKey(Forum,
                                on_delete=models.CASCADE)
    comment = models.TextField()
    posted_on = models.DateField(auto_now=True)
    last_edit = models.DateField(auto_now_add=True)
    comment_by = models.ForeignKey(UserProfile,
                                    on_delete=models.PROTECT)
    reply_to = models.ForeignKey('ForumComment',
                                blank=True,
                                null=True,
                                on_delete=models.PROTECT)
    
    def __str__(self):
        return self.forum.title
    
    def get_reply(self):
        try:
            comments = []
            replies = ForumComment.objects.filter(reply_to=self.id)
            for r in replies:
                comments.append({'comment': r.comment, 'posted_on': r.posted_on, 'comment_by': r.comment_by, 'replies': r.get_reply})
            
            return comments
        except:
            return None