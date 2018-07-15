import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def user_profile(request, user_id):
    pass
