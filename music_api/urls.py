"""
URL configuration for music_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from tracks.views import *
from tracks import views

router = DefaultRouter()
#outer.register(r"tracks", TrackViewSet, basename="tracks")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("tracks.urls")),

    # Pages (HTML)
    path("", views.home_page, name="home"),
    path("create/", views.create_track_page, name="create-track-page"),
    path("delete/", views.delete_track_page, name="delete-track-page"),
    path("search/", views.search_track_page, name="search-track-page"),
    path("update/", views.update_track_page, name="update-track-page"),
    path("averages/", views.genre_averages_page, name="genre-averages-page"),
    path("moods/", views.mood_tracks_page, name="mood-tracks-page"),

    # API (JSON)
    path("api/tracks/", views.track_list_api),
    path("api/tracks/create/", views.create_track_api),
    path("api/tracks/<int:track_id>/", views.delete_track_api),
    path("api/tracks/search/", views.search_tracks_api),
    path("api/track/<int:track_id>/", get_track_api, name="get_track_api"),
    path("api/track/<int:track_id>/update/", update_track_api),
    path("api/genres/<str:genre>/averages/", genre_averages_api),
    path("api/moods/<str:mood>/", mood_tracks_api),



]


