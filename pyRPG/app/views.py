import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import models

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
    characters = models.Character.objects.filter(user=user)
    print campaigns
    context = {
        'user': user,
        'campaigns': campaigns,
        'characters': characters
    }
    return render(request,
                  'profile/index.html',
                  context)

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
    print chapters
    context = {
        'user': user,
        'campaign': campaign,
        'chapters': chapters
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
    # create new enemy
    if request.is_ajax and 'new_enemy' in request.POST:
        attack_type = models.Attack.objects.get(id=request.POST.get('attack_type'))
        sub_attack_type = models.Attack.objects.get(id=request.POST.get('sub_attack_type'))
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
            inventory = request.POST.get('inventory'),
            inventory_limit = request.POST.get('name'),
            exp = request.POST.get('name'),
            initiation = request.POST.get('name'),
            attack = request.POST.get('name'),
            user = campaign.host,
            attack_type = attack_type,
            sub_attack_type = sub_attack_type,
            enemy = True,
            enemy_type = request.POST.get('enemy_type')
        )
        new_enemy.save()
        return HttpResponse(new_enemy)
    # use existing enemy list

    # create new NPC

    # start battle

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
