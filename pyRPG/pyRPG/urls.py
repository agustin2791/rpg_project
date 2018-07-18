"""pyRPG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^profile/(?P<username>\w{0,50})/$',
        views.user_profile,
        name='profile'),

    # Campaign
    url(r'^profile/(?P<username>\w{0,50})/campaign/create/$',
        views.create_campaign,
        name='create_campaign'),
    url(r'^profile/(?P<username>\w{0,50})/campaign/create/submit/$',
        views.create_campaign_submit,
        name='create_campaign_submit'),
    url(r'^profile/(?P<username>\w{0,50})/campaign/(?P<campaign_id>[0-9])/edit/$',
        views.campaign_edit,
        name='campaign_edit'),
    url(r'^admin/', admin.site.urls),
]
