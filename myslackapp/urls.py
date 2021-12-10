"""myslackapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Set this flag to False if you want to enable oauth_app instead
is_simple_app = True

if is_simple_app:
    # A simple app that works only for a single Slack workspace
    # (prerequisites)
    # export SLACK_BOT_TOKEN=
    # export SLACK_SIGNING_SECRET=
    from simple_app.urls import slack_events_handler

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("slack/events", slack_events_handler),
        path("ohmuffin/", include("ohmuffin.urls")),
    ]

