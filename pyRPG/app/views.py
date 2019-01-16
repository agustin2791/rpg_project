import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Prefetch
# from django.views.generic import Views
import json

import models
import forms

def registration(request):
    if request.user.is_authenticated:
        return redirect('/profile/{0}'.format(request.user.username))
    if request.is_ajax and 'new_user' in request.POST:
        print request.POST
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        new_email = request.POST.get('email')
        user = User.objects.create_user(
            email=new_email,
            username=new_username,
            password=new_password
        )
        user.save()
        print user
        user_profile = models.UserProfile.objects.create(
            user=user
        )
        user_profile.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                redirect_url = '/profile/{0}/'.format(user.username)
                return HttpResponse(redirect_url)

    return render(request, 'authentication/register.html')

def user_login(request):
    login_form = forms.UserLogin(request.POST)
    if request.user.is_authenticated:
        return redirect('/profile/{0}'.format(request.user.username))

    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile/{0}/'.format(user.username))
    return render(request,
                  'authentication/login.html',
                  {'form': login_form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')

ALIGNMENTS = (
    ('lg','Lawful Good'),
    ('ng', 'Natural Good'),
    ('cg', 'Chaotic good'),
    ('ln', 'Lawful Neutral'),
    ('tn', 'True Neutral'),
    ('cn','Chaotic Neutral'),
    ('le', 'Lawful Evil'),
    ('ne', 'Neutral Evil'),
    ('ce', 'Chaotic Evil')
)
SKILLS = {
    ('acrobatics', 'Acrobatics'),
    ('anima_hand', 'Animal Handling'),
    ('arcana', 'Arcana'),
    ('athletics', 'Athletics'),
    ('deception', 'Deception'),
    ('history', 'History'),
    ('insight', 'Insight'),
    ('intimidation', 'Intimidation'),
    ('investigation', 'Investigation'),
    ('medicine', 'Medicine'),
    ('nature', 'Nature'),
    ('perception', 'Perception'),
    ('performance', 'Performance'),
    ('persuasion', 'Persuasion'),
    ('religion', 'Religion'),
    ('soh', 'Slight if Hand'),
    ('stealth', 'Stealth'),
    ('survival', 'Survival')
}
def get_alignment(alignment):
    if alignment == 'lg':
        name = 'Lawful Good'
        description = 'Creatures can be counted on to do the right thing as expected by society. Gold dragons, paladins, and most dwarves are lawful good.'
    elif alignment == 'ng':
        name = 'Natural Good'
        description = 'Folk do the best they can to help others according to their needs. Many celestials, some cloud giants, and most gnomes are neutral good.'
    elif alignment == 'cg':
        name = 'Chaotic good'
        description = 'Creatures act as their conscience directs, with little regard for what others expect. Copper dragons, many elves, and unicorns are chaotic good.'
    elif alignment == 'ln':
        name = 'Lawful Neutral'
        description = 'Individuals act in accordance with law, tradition, or personal codes. Many monks and some wizards are lawful neutral.'
    elif alignment == 'tn':
        name ='True Neutral'
        description = 'Is the alignment of those who prefer to steer clear of moral questions and don\'t take sides, doing what seems best at the time. Lizardfolk, most druids, and many humans are neutral.'
    elif alignment == 'cn':
        name = 'Chaotic Neutral'
        description = 'Creatures follow their whims, holding their personal freedom above all else. Many barbarians and rogues, and some bards, are chaotic neutral.'
    elif alignment == 'le':
        name = 'Lawful Evil'
        description = 'Creatures methodically take what they want, within the limits of a code of tradition, loyalty, or order. Devils, blue dragons, and hobgoblins are lawful evil.'
    elif alignment == 'ne':
        name = 'Neutral Evil'
        description = 'Is the alignment of those who do whatever they can get away with, without compassion or qualms. Many drow, some cloud giants, and goblins are neutral evil.'
    elif alignment == 'ce':
        name = 'Chaotic Evil'
        description = 'Creatures act with arbitrary violence, spurred by their greed, hatred, or bloodlust. Demons, red dragons, and orcs are chaotic evil.'
    return '{0}: {1}'.format(name, description)

def get_modifier(score):
    score = int(score)
    if score == 1:
        score_mod = -5
    elif score >= 30:
        score_mod = 10
    else:
        score_mod = (score/2) - 5

    return score_mod

def character_skills(char):
    character = models.Character.objects.get(id=char)
    skills_list = {
        'strength': get_modifier(character.strength),
        'dexterity': get_modifier(character.dexterity),
        'intelligence': get_modifier(character.intelligence),
        'charisma': get_modifier(character.charisma),
        'wisdom': get_modifier(character.wisdom)
    }
    if character.skill_set:
        skill = character.skill_set.lower().split(', ')
        for s in skill:
            skills_list[s] += character.proficiency_bonus

    skills = models.CharacterSkills.objects.update_or_create(
        character=character,
        defaults={
            'acrobatics':skills_list['dexterity'],
            'anima_hand':skills_list['wisdom'],
            'arcana':skills_list['intelligence'],
            'athletics':skills_list['strength'],
            'deception':skills_list['charisma'],
            'history':skills_list['intelligence'],
            'insight':skills_list['wisdom'],
            'intimidation':skills_list['charisma'],
            'investigation':skills_list['intelligence'],
            'medicine':skills_list['wisdom'],
            'nature':skills_list['intelligence'],
            'perception':skills_list['wisdom'],
            'performance':skills_list['charisma'],
            'persuasion':skills_list['charisma'],
            'religion':skills_list['intelligence'],
            'soh':skills_list['dexterity'],
            'stealth':skills_list['dexterity'],
            'survival':skills_list['wisdom']
        }
    )[0]
    skills.save()

def get_all_items(character):
    inventory = []
    if character.inventory.count() > 0:
        for c in character.inventory.all():
            inventory.append(c.id)
    ag1 = models.Item.objects.filter(category__name='Adventure Grear').exclude(id__in=inventory)
    ag2 = models.Item.objects.filter(category__name='Ammunition').exclude(id__in=inventory)
    ag3 = models.Item.objects.filter(category__name='Arcane Focus').exclude(id__in=inventory)
    ag4 = models.Item.objects.filter(category__name='Druid Focus').exclude(id__in=inventory)
    ag5 = models.Item.objects.filter(category__name='Holy Symbol').exclude(id__in=inventory)
    armor1 = models.Item.objects.filter(category__name__contains='Armor').exclude(id__in=inventory)
    armor2 = models.Item.objects.filter(category__name='Shield').exclude(id__in=inventory)
    mounts1 = models.Item.objects.filter(category__name='Mounts').exclude(id__in=inventory)
    mounts2 = models.Item.objects.filter(category__name__contains='Vehicle').exclude(id__in=inventory)
    mounts3 = models.Item.objects.filter(category__name='Saddles').exclude(id__in=inventory)
    tools1 = models.Item.objects.filter(category__name__contains='Tools').exclude(id__in=inventory)
    tools2 = models.Item.objects.filter(category__name='Gaming Set').exclude(id__in=inventory)
    tools3 = models.Item.objects.filter(category__name='Musical Instrument').exclude(id__in=inventory)
    weapons = models.Item.objects.filter(category__name__contains='Weapons').exclude(id__in=inventory).order_by('name')
    ag = ag1 | ag2 | ag3 | ag4 | ag5
    armor = armor1 | armor2
    mounts = mounts1 | mounts2 | mounts3
    tools = tools1 | tools2 | tools3

    return [ag.order_by('name'), armor.order_by('name'), mounts.order_by('name'), tools.order_by('name'), weapons.order_by('name')]

def index(request):
    return render(request, 'index.html')

def send_request(request):
    if request.is_ajax and request.POST:
        user = User.objects.get(id=request.POST['user'])
        sender = User.objects.get(id=request.POST['sender'])
        sender.friend_request.add(user)
        return HttpResponse('Request Sent')

def request_approval(request):
    if request.is_ajax and request.POST:
        user = User.objects.get(id=request.POST['user'])
        approver = User.objects.get(id=request.POST['approver'])
        approver.friends_list.add(user)
        approver.friend_request.remove(user)
        return HttpResponse('Approved')

def user_profile(request, username):
    user = User.objects.get(username=username)
    campaigns = models.Campaign.objects.filter(host=user)
    characters = models.Character.objects.filter(user=user, enemy=False)

    context = {
        'user': user,
        'campaigns': campaigns,
        'characters': characters
    }
    return render(request,
                  'profile/index.html',
                  context)

def character_creation(request, username):
    user = User.objects.get(username=username)
    classes = models.CharacterClass.objects.all().order_by('name')
    races = models.CharacterRace.objects.all().order_by('name')
    alignments = ALIGNMENTS

    # Get Character Class Details
    if request.is_ajax and 'character_class' in request.POST:
        cc = models.CharacterClass.objects.get(id=request.POST.get('c_class'))
        context = {'cc': cc}
        return render(request,
                      'profile/character/class_details.html',
                      context)
    # Get Character Race details
    if request.is_ajax and 'character_race' in request.POST:
        cr = models.CharacterRace.objects.get(id=request.POST.get('c_race'))
        traits = models.CharacterRaceTraits.objects.filter(char_race__id=cr.id)
        context = {'cr': cr, 'traits': traits}
        return render(request,
                      'profile/character/race_details.html',
                      context)

    if request.is_ajax and 'new_character' in request.POST:
        char_class = models.CharacterClass.objects.get(id=request.POST.get('c_class'))
        char_race = models.CharacterRace.objects.get(id=request.POST.get('c_race'))
        alignment = get_alignment(request.POST.get('alignment'))
        character = models.Character.objects.create(
            name=request.POST.get('name'),
            c_class=char_class,
            c_race=char_race,
            level=request.POST.get('level'),
            hp=request.POST.get('hit_points'),
            full_hp=request.POST.get('hit_points'),
            speed=request.POST.get('speed'),
            strength=request.POST.get('strength'),
            dexterity=request.POST.get('dex'),
            constitution=request.POST.get('cons'),
            intelligence=request.POST.get('int'),
            charisma=request.POST.get('charm'),
            wisdom=request.POST.get('wisdom'),
            alignment=alignment,
            hit_dice=char_class.hit_dice,
            saving_throws=char_class.saving_throws,
            user=user
        )
        character_level = models.CharacterClassLevel.objects.get(char_class=char_class, level=character.level)
        character.proficiency_bonus = character_level.pro_bonus
        character.save()
        character_skills(character.id)
        currency = models.CharacterCurrency.objects.create(character=character)
        redirect_to = '/profile/{0}/character_info/{1}/'.format(user.username, character.id)
        return HttpResponse(redirect_to)

    context = {
        'user': user,
        'classes': classes,
        'races': races,
        'alignments': alignments
    }
    return render(request,
                  'profile/character/create.html',
                  context)

def character_info(request, username, char_id):
    user = User.objects.get(username=username)
    character = models.Character.objects.get(pk=char_id)
    skills = models.CharacterSkills.objects.get(character=character)
    char_class = models.CharacterClass.objects.get(id=character.c_class.id)
    char_race = models.CharacterRace.objects.get(id=character.c_race.id)
    char_features = models.CharacterFeature.objects.filter(character=character)
    background = models.CharacterBackground.objects.filter(character=character)
    ag, armor, mounts, tools, weapons = get_all_items(character)

    # Edit background, features, etc...
    if request.is_ajax and 'add_feature' in request.POST:
        trait = request.POST.get('trait')
        description = request.POST.get('description')
        if trait == 'background':
            character.background_skills = description
            character.save()
            return render(request,
                      'profile/character/info/background.html',
                      {'character': character})
        elif trait.startswith('feature'):
            feat_id = trait.split('_')[1]
            feature = models.CharacterFeature.objects.get(id=feat_id)
            feature.description = description
            feature.save()
            char_features = models.CharacterFeature.objects.filter(character=character)
            return render(request,
                          'profile/character/info/features.html',
                          {
                            'features': char_features,
                            'character': character
                          })
        elif trait == 'equipment':
            setattr(character, 'equipment', description)
            character.save()
            return render(request,
                          'profile/character/info/equipment.html',
                          {'character': character})
        else:
            setattr(character, trait, description)
            character.save()
            return render(request,
                        'profile/character/info/traits.html',
                        {'character': character})
    # Add Feature or Background
    if request.is_ajax and 'new_feature' in request.POST:
        feature_name = request.POST.get('name')
        feature_description = request.POST.get('desc')
        object_edit = request.POST.get('object')
        if object_edit == 'feature':
            new_feature = models.CharacterFeature.objects.create(
                feature=feature_name,
                description=feature_description,
                character=character
            )
            new_feature.save()
            char_features = models.CharacterFeature.objects.filter(character=character)
            return render(request,
                          'profile/character/info/features.html',
                          {'features': char_features})
        if object_edit == 'background':
            skills = request.POST.get('skills')
            character.background = feature_name
            character.background_skills = feature_description
            if character.skill_set:
                skill_set = character.skill_set
                skill_set = skill_set.split(', ')
                new_skills = skills.split(', ')
                all_skills = skill_set + new_skills
                character.skill_set = all_skills.join(', ')
            else:
                character.skill_set = skills
            character.save()
            return render(request,
                          'profile/character/info/background.html',
                          {'character': character})
    # Remove feature
    if request.is_ajax and 'remove_feat' in request.POST:
        feat = models.CharacterFeature.objects.get(id=request.POST.get('feat'))
        feat.delete()
        features = models.CharacterFeature.objects.filter(character=character)
        return render(request,
                      'profile/character/info/features.html',
                      {'features': features})

    # Add Skills
    if request.is_ajax and 'add_skills' in request.POST:
        skills = request.POST.get('skills')
        if character.skill_set:
            char_skills = character.skill_set
            char_skills = char_skills.split(', ')
            new_skills = skills.split(', ')
            all_skills = char_skills + new_skills
            character.skill_set = ', '.join(all_skills)
        else:
            character.skill_set = skills
        character.save()
        skills = models.CharacterSkills.objects.get(character=character)
        return render(request,
                      'profile/character/info/skills.html',
                      {'character': character,
                      'skills': skills})

    # Add Equipment
    if request.is_ajax and 'add_equipment' in request.POST:
        equipment = request.POST.getlist('equip[]')
        for e in equipment:
            equip = models.Item.objects.get(id=e)
            character.inventory.add(equip)
            character.save()
        redirect_to = '/profile/{0}/character_info/{1}/'.format(user, character.id)
        return HttpResponse(redirect_to)

    # Add Spell
    if request.is_ajax and 'add_spell' in request.POST:
        spell = models.Spells.objects.get(id=request.POST.get('spell'))
        character.spells.add(spell)
        character.save()
        return render(request,
                      'profile/character/info/spells.html',
                      {'character': character})

    # Remove equipment, feature, spells
    if request.is_ajax and 'remove' in request.POST:
        subject = request.POST.get('subject')
        item = request.POST.get('item')
        if subject == 'equip':
            e = models.Item.objects.get(id=item)
            character.inventory.remove(e)
            character.save()
            return render(request,
                          'profile/character/info/equipment.html',
                          {'character': character})
        if subject == 'feat':
            feat = models.CharacterFeature.objects.get(id=item).delete()
            features = models.CharacterFeature.objects.filter(character=character)
            return render(request,
                          'profile/character/info/features.html',
                          {'features': features})
        if subject == 'spell':
            spell = models.Spells.objects.get(id=item)
            character.spells.remove(spell)
            character.save()
            return render(request,
                          'profile/character/info/spells.html',
                          {'character': character})

    context = {
        'user': user,
        'character': character,
        'skills': skills,
        'char_class': char_class,
        'char_race': char_race,
        'features': char_features,
        'items': [ag, armor, mounts, tools, weapons],
        'background': background
    }
    return render(request,
                  'profile/character/edit.html',
                  context)

# CREATE, EDIT, AND START CAMPAIGN
# Create campaign
def create_campaign(request, username):
    user = User.objects.get(username=username)

    return render(request,
                  'campaign/create.html')

# Submitting the campaign and finish the campaign creation
def create_campaign_submit(request, username):
    user = User.objects.get(username=username)
    if request.is_ajax and request.POST:
        new_campaign = models.Campaign.objects.create(
            name=request.POST.get('name'),
            slug=request.POST.get('slug'),
            host=user,
            player_limit=request.POST.get('player_limit'),
            objective=request.POST.get('obj'),
            beginning=request.POST.get('start'),
            end=request.POST.get('end'),
        )
        new_campaign.save()
        redirect_to = '/campaign/{0}/{1}/edit/'.format(username, new_campaign.slug)
        return HttpResponse(redirect_to)

# Edit the campaign
def campaign_edit(request, username, slug):
    user = User.objects.get(username=username)
    campaign = models.Campaign.objects.get(host=user, slug=slug)
    chapters = models.CampaignChapter.objects.filter(campaign__host=user, campaign=campaign)
    battles = models.Battle.objects.filter(campaign=campaign)
    npcs = models.NonPlayableCharacters.objects.filter(campaign=campaign)

    try:
        enemies = campaign.getEnemies
    except:
        enemies = None
    print enemies
    # Invite players

    if request.is_ajax and 'call_modal' in request.POST:
        modal = request.POST.get('form')
        context = {'campaign': campaign}
        return render(request,
                      'campaign/forms/{0}.html'.format(modal),
                      context)
    # create new enemy
    if request.is_ajax and 'new_enemy' in request.POST:
        print 'new_enemy'
        # attack_type = models.Attack.objects.get(id=request.POST.get('attack_type'))
        # sub_attack_type = models.Attack.objects.get(id=request.POST.get('sub_attack_type'))
        new_enemy = models.Character.objects.create(
            name = request.POST.get('name'),
            hp = request.POST.get('hp'),
            full_hp = request.POST.get('hp'),
            damage = request.POST.get('damage'),
            speed = request.POST.get('speed'),
            defence = request.POST.get('defence'),
            dexterity = request.POST.get('dex'),
            constitution = request.POST.get('constitution'),
            intelligence = request.POST.get('intelligence'),
            charisma = request.POST.get('charm'),
            wisdom = request.POST.get('wisdom'),
            user = campaign.host,
            enemy = True,
            enemy_type = request.POST.get('enemy_type'),
            attack=0
        )
        new_enemy.save()
        # creates the enemy's action
        new_actions = models.CharacterFeature.objects.create(
            feature='Actions',
            description=request.POST.get('actions'),
            character=new_enemy
        )
        # creating additional information for the enemy
        if request.POST.getlist('additional-info[]') != None:
            list = request.POST.get('additional-info')
            add_list = request.POST.getlist('additional-info[]')
            json_list = json.loads(add_list[0])
            for i in json_list:
                char_info = models.CharacterFeature.objects.create(
                    feature=i[u'name'],
                    description=i[u'description'],
                    character=new_enemy
                )
        campaign.characters.add(new_enemy)
        campaign.save()
        context = {'enemies': campaign.getEnemies}
        return render(request,
                      'campaign/components/camp_enemies.html',
                      context)
    # use existing enemy list

    # Create Battle
    if request.is_ajax and 'new_campaign_battle' in request.POST:
        new_battle = models.Battle.objects.create(
            name=request.POST.get('name'),
            number_of_commoner=request.POST.get('commoners'),
            description=request.POST.get('description'),
            campaign=campaign
        )
        enemies = request.POST.getlist('enemies[]')
        try:
            for e in enemies:
                print int(e)
                enemy = models.Character.objects.get(id=int(e))
                new_battle.enemies.add(enemy)
        except:
            pass

        try:
            for c in campaign.characters:
                if c.enemy == False:
                    new_battle.characters.add(c)
        except:
            pass
        battles = models.Battle.objects.filter(campaign=campaign)
        context = {'battles': battles}
        return render(request,
                      'campaign/components/camp_battles.html',
                      context)

    # create new NPC
    if request.is_ajax and 'new_campaign_npc' in request.POST:
        new_npc = models.NonPlayableCharacters.objects.create(
            name=request.POST.get('name'),
            script=request.POST.get('dialog'),
            campaign=campaign
        )
        new_npc.save()
        npcs = models.NonPlayableCharacters.objects.filter(campaign=campaign)
        context = {'npcs': npcs}
        return render(request,
                      'campaign/components/camp_npc.html',
                      context)

    context = {
        'user': user,
        'campaign': campaign,
        'chapters': chapters,
        'enemies': enemies,
        'battles': battles,
        'npcs': npcs
    }
    return render(request,
                  'campaign/edit.html',
                  context)

# Creates a new chapter of a campaign
def new_campaign_chapter(request, username, slug, campaign_id):
    user = User.objects.get(username=username)
    campaign = models.Campaign.objects.get(id=campaign_id,
                                           host__username=username,
                                           slug=slug)
    print campaign

    context = {
        'user': user,
        'campaign': campaign
    }

    return render(request,
                  'campaign/new_chapter.html',
                  context)

# Submits and creates the chapter of the campaign
def submit_campaign_chapter(request, username, slug, campaign_id):
    user = User.objects.get(username=username)
    campaign = models.Campaign.objects.get(id=campaign_id,
                                           host__username=username,
                                           slug=slug)

    if request.is_ajax and request.POST:
        new_chapter = models.CampaignChapter.objects.create(
            name=request.POST.get('name'),
            slug=request.POST.get('slug'),
            description=request.POST.get('desc'),
            campaign=campaign
        )
        new_chapter.save()
        print '\n'
        print 'New Chapter: ', new_chapter
        redirect_to = '/campaign/{0}/{1}/chapter/{2}/edit/'.format(username, campaign.slug, new_chapter.slug)
        return HttpResponse(redirect_to)

# Edit the Campaign's chapter
def edit_campaign_chapter(request, username, campaign_slug, chapter_slug, chapter_id):
    user = User.objects.get(username=username)
    campaign = models.Campaign.objects.get(host__username=username,
                                           slug=campaign_slug)
    chapter = models.CampaignChapter.objects.get(id=chapter_id,
                                                 campaign__host__username=username,
                                                 campaign__slug=campaign_slug,
                                                 slug=chapter_slug)

    context = {
        'user': user,
        'campaign': campaign
    }

    return render(request,
                  'campaign/edit_chapter.html',
                  context)

def campaign(request, username, slug, campaign_id):
    campaign = models.Campaign.objects.get(id=campaign_id,
                                           host__username=username,
                                           slug=slug)
    # create character class
    if request.is_ajax and 'new_character_class' in request.POST:
        new_class = models.CharacterClass.objects.create(
            name = request.POST.get('name'),
            enemy = False
        )
        new_class.save()
        return HttpResponse(new_class)
    # create character race
    if request.is_ajax and 'new_character_race' in request.POST:
        new_race = models.CharacterClass.objects.create(
            name = request.POST.get('name'),
            enemy = True
        )
        new_race.save()
        return HttpResponse(new_race)

    enemies = models.CampaignEnemies.objects.filter(campaign=campaign)
    context = {
        'campaign': campaign,
        'enemies': enemies
    }
    return render(request,
                  'campaign/index.html',
                  context)


# global values
def global_context(request):
    login_form = forms.UserLogin
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
    else:
        user = None

    context = {
        'user': user,
        'user_login': login_form
    }
    return context
