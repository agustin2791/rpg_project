import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Prefetch
import json

import models

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

    if request.is_ajax and 'add_feature' in request.POST:
        trait = request.POST.get('trait')
        description = request.POST.get('description')
        if trait == 'personality_traits':
            character.personality_traits = description
        elif trait == 'ideals':
            character.ideals = description
        elif trait == 'bonds':
            character.bonds = description
        elif trait == 'flaws':
            character.flaws = description
        elif trait == 'equipment':
            character.equipment = description
        else:
            new_trait = models.CharacterFeature.objects.create(
                feature=trait,
                description=description,
                character=character
            )
        character.save()
        return render(request,
                      'profile/character/info/traits.html',
                      {'character': character})

    if request.is_ajax and 'new_feature' in request.POST:
        feature_name = request.POST.get('name')
        feature_description = request.POST.get('desc')
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

    if request.is_ajax and 'background_skills' in request.POST:
        all_skills = ['acrobatics', 'anima_hand', 'arcana', 'athletics', 'deception', 'history', 'insight', 'intimidation', 'investigation', 'medicine', 'nature', 'perception', 'performance', 'persuasion', 'religion', 'soh', 'stealth', 'survival']

    context = {
        'user': user,
        'character': character,
        'skills': skills,
        'char_class': char_class,
        'char_race': char_race,
        'features': char_features
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
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
    else:
        user = None

    context = {
        'user': user
    }
    return context
