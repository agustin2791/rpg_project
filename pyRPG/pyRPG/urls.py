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
    # Authentication
    url(r'^authenticate/register$',
        views.registration,
        name="register"),
    url(r'^authenticate/login$',
        views.user_login,
        name='login'),
    url(r'^authenticate/logout$',
        views.user_logout,
        name='logout'),
    url(r'^profile/(?P<username>\w{0,50})/$',
        views.user_profile,
        name='profile'),

    # Character creation
    url(r'^profile/(?P<username>\w{0,50})/character_creation/$',
        views.character_creation,
        name='character_creation'),
    url(r'^profile/(?P<username>\w{0,50})/character_info/(?P<char_id>\d+)/$',
        views.character_info,
        name='character_info'),
    url(r'^profile/(?P<username>\w{0,50})/character_info/(?P<char_id>\d+)/image_upload/$',
        views.character_upload_image,
        name='upload_image'),
    # Campaign
    url(r'^campaign/(?P<username>\w{0,50})/(?P<slug>[\w-]+)/(?P<campaign_id>\d+)/play/$',
        views.campaign,
        name="campaign"),
    url(r'^campaign/(?P<username>\w{0,50})/create/$',
        views.create_campaign,
        name='create_campaign'),
    # Submit the campaign
    url(r'^campaign/(?P<username>\w{0,50})/create/submit/$',
        views.create_campaign_submit,
        name='create_campaign_submit'),
    # Edit campaign
    url(r'^campaign/(?P<username>\w{0,50})/(?P<slug>[\w-]+)/edit/$',
        views.campaign_edit,
        name='campaign_edit'),
    # create new campaign chapter
    url(r'^campaign/(?P<username>\w{0,50})/(?P<slug>[\w-]+)/(?P<campaign_id>\d+)/chapter/new/$',
        views.new_campaign_chapter,
        name='new_campaign_chapter'),
    # submit new campaign chapter
    url(r'^campaign/(?P<username>\w{0,50})/(?P<slug>[\w-]+)/(?P<campaign_id>\d+)/chapter/submit/$',
        views.submit_campaign_chapter,
        name='submit_campaign_chapter'),
    url(r'^campaign/(?P<username>\w{0,50})/(?P<campaign_slug>[\w-]+)/chapter/(?P<chapter_slug>[\w-]+)/(?P<chapter_id>\d+)/edit/$',
        views.edit_campaign_chapter,
        name='edit_campaign_chapter'),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)