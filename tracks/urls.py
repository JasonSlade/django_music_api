# tracks/urls.py
from django.urls import path
from .views import TrackList, TrackDetail

urlpatterns = [
    path("tracks/", TrackList.as_view(), name="track-list"),
    path("tracks/<int:pk>/", TrackDetail.as_view(), name="track-detail"),
]
