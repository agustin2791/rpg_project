import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')

def user_profile(request, username):
    user = User.objects.get(username=username)

    context = {
        user: user
    }
    return render(request,
                  'profile/index.html',
                  context)

def create_campaign(request, username):
    user = User.objects.get(username=username)

    return render(request,
                  'campaign/create.html')
