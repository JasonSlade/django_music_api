# tracks/urls.py


from django.urls import path
from .views import (
    track_list_api,
    create_track_api,
    get_track_api,
    update_track_api,
    delete_track_api,
)

urlpatterns = [
    path("tracks/", track_list_api),
    path("tracks/create/", create_track_api),
    path("tracks/<int:track_id>/", get_track_api),
    path("tracks/<int:track_id>/update/", update_track_api),
    path("tracks/<int:track_id>/delete/", delete_track_api),
]
