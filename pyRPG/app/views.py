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
    print campaigns
    context = {
        'user': user,
        'campaigns': campaigns
    }
    return render(request,
                  'profile/index.html',
                  context)

def create_campaign(request, username):
    user = User.objects.get(username=username)

    return render(request,
                  'campaign/create.html')

def create_campaign_submit(request, username):
    user = User.objects.get(username=username)
    print request.POST
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

def campaign_edit(request, username, slug):
    user = User.objects.get(username=username)
    campaign = models.Campaign.objects.get(host=user, slug=slug)
    chapters = models.CampaignChapter.objects.filter(campaign__host=user)
    context = {
        'user': user,
        'campaign': campaign,
        'chapters': chapters
    }
    return render(request,
                  'campaign/edit.html',
                  context)

def new_campaign_chapter(request, username, slug):
    user = User.objects.get(username=username)
    campaign = models.Campaign.objects.get(host__username=username, slug=slug)

    context = {
        'user': user,
        'campaign': campaign
    }

    return render(request,
                  'campaign/new_chapter.html',
                  context)

def submit_campaign_chapter(request, username, slug):
    user = User.objects.get(username=username)
    campaign = models.Campaign.objects.get(host__username=username, slug=slug)

    if request.is_ajax and request.POST:
        new_chapter = models.CampaignChapter.objects.create(
            name=request.POST.get('name'),
            slug=request.POST.get('slug'),
            description=request.POST.get('desc'),
            campaign=campaign
        )
        new_chapter.save()
        redirect_to = '/campaign/{0}/{1}/chapter/{2}/edit/'.format(username, campaign.slug, new_chapter.slug)
        return HttpResponse(redirect_to)

def edit_campaign_chapter(request, username, campaign_slug, chapter_slug):
    user = User.objects.get(username=username)
    campaign = models.Campaign.objects.get(host__username=username,
                                           slug=cmapaign_slug)
    chapter = models.CampaignChapter.objects.get(campaign__host__username=username,
                                                 campaign_slug=campaign_slug,
                                                 slug=chapter_slug)

    context = {
        'user': user,
        'campaign': campaign
    }

    return render(request,
                  'campaign/edit_chapter.html',
                  context)
