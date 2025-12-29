from django.shortcuts import render

import json

from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Track
from .serializers import TrackSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.views.decorators.csrf import ensure_csrf_cookie


from django.http import JsonResponse
from django.db.models import Avg


from django.db.models import Q

# Create your views here.

# Home page:
def home_page(request):
    return render(request, "tracks/home.html")




@ensure_csrf_cookie
def create_track_page(request):
    return render(request, "tracks/create_track.html")

def delete_track_page(request):
    return render(request, "tracks/delete_track.html")

def search_track_page(request):
    return render(request, "tracks/search_track.html")

def update_track_page(request):
    return render(request, "tracks/update_track.html")

def genre_averages_page(request):
    return render(request, "tracks/average_genre.html")

def mood_tracks_page(request):
    return render(request, "tracks/mood_tracks.html")



def create_track_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        track = Track.objects.create(
            genre=data.get("genre"),
            artist_name=data.get("artist_name"),
            track_name=data.get("track_name"),
            popularity=data.get("popularity"),
            acousticness=data.get("acousticness"),
            danceability=data.get("danceability"),
            duration_ms=data.get("duration_ms"),
            energy=data.get("energy"),
            instrumentalness=data.get("instrumentalness"),
        )

        return JsonResponse(
            {"id": track.id},
            status=201
        )

    return JsonResponse({"error": "Method not allowed"}, status=405)

def delete_track_api(request, track_id):
    if request.method == "DELETE":
        track = Track.objects.get(id=track_id)
        track.delete()
        return JsonResponse(
            {"message": "Track deleted"},
            status=204
        )

def search_tracks_api(request):
    track_name = request.GET.get("track_name", "")
    artist_name = request.GET.get("artist_name", "")
    genre = request.GET.get("genre", "")
    popularity = request.GET.get("popularity", "")

    tracks = Track.objects.all()

    if track_name:
        tracks = tracks.filter(track_name__icontains=track_name)

    if artist_name:
        tracks = tracks.filter(artist_name__icontains=artist_name)

    if genre:
        tracks = tracks.filter(genre__icontains=genre)

    if popularity is not None and popularity != "":
        tracks = tracks.filter(popularity__gte=int(popularity))


    results = list(tracks.values(
        "id",
        "track_name",
        "artist_name",
        "genre",
        "popularity",
        "danceability",
        "energy",
        "acousticness",
        "instrumentalness",
        "duration_ms"
    ))

    return JsonResponse(results, safe=False)

##################################################################################################################

# get track by ID
# re use our search function api to load the track we want to update 
def get_track_api(request, track_id):
    if request.method == "GET":
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return JsonResponse({"error": "Track not found"}, status=404)

        return JsonResponse({
            "id": track.id,
            "genre": track.genre,
            "artist_name": track.artist_name,
            "track_name": track.track_name,
            "popularity": track.popularity,
            "acousticness": track.acousticness,
            "danceability": track.danceability,
            "duration_ms": track.duration_ms,
            "energy": track.energy,
            "instrumentalness": track.instrumentalness,
        })


def update_track_api(request, track_id):
    if request.method == "POST":
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return JsonResponse({"error": "Track not found"}, status=404)

        data = json.loads(request.body)

        track.genre = data.get("genre", track.genre)
        track.artist_name = data.get("artist_name", track.artist_name)
        track.track_name = data.get("track_name", track.track_name)
        track.popularity = data.get("popularity", track.popularity)
        track.acousticness = data.get("acousticness", track.acousticness)
        track.danceability = data.get("danceability", track.danceability)
        track.duration_ms = data.get("duration_ms", track.duration_ms)
        track.energy = data.get("energy", track.energy)
        track.instrumentalness = data.get("instrumentalness", track.instrumentalness)

        track.save()

        return JsonResponse({"id": track.id}, status=200)
    
##################################################################################################################################


def genre_averages_api(request, genre):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    queryset = Track.objects.filter(genre__iexact=genre)

    if not queryset.exists():
        return JsonResponse(
            {"error": "Genre not found"},
            status=404
        )

    # averages is a python function
    # our values are 'primitive' types eg: float
    # JsonResponse converts these python vals to a Json
    # this conversion step is the process of serialisation
    averages = queryset.aggregate(
        popularity=Avg("popularity"),
        acousticness=Avg("acousticness"),
        danceability=Avg("danceability"),
        energy=Avg("energy"),
        instrumentalness=Avg("instrumentalness"),
        duration_ms=Avg("duration_ms"),
    )

    return JsonResponse({
        "genre": genre,
        "averages": averages
    })
##################################################################################################################################
# get 'mood' tracks api
# Chill | Happy | Sad

def mood_tracks_api(request, mood):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    mood = mood.lower()

    if mood == "chill":
        queryset = Track.objects.filter(
            energy__lt=0.4,
            danceability__lt=0.5,
            acousticness__gt=0.4
        )

    elif mood == "happy":
        queryset = Track.objects.filter(
            energy__gt=0.6,
            danceability__gt=0.6,
            instrumentalness__lt=0.2
        )

    elif mood == "sad":
        queryset = Track.objects.filter(
            energy__lt=0.4,
            danceability__lt=0.5,
            duration_ms__gt=180000,
            acousticness__gt=0.3
        )
    elif mood == "excited":
        queryset = Track.objects.filter(
            energy__gt=0.7,
            danceability__gt=0.7,
            popularity__gt=70
        )
    elif mood == "study":
        queryset = Track.objects.filter(
            instrumentalness__gt=0.5,
            energy__lt=0.5,
            acousticness__gt=0.4
        )
    elif mood == "workout":
        queryset = Track.objects.filter(
            energy__gt=0.6,
            danceability__gt=0.6,
            duration_ms__gt=150000
        )
    elif mood == "romantic":
        queryset = Track.objects.filter(
            acousticness__gt=0.5,
            energy__lt=0.5,
            danceability__gt=0.4
        )

    else:
        return JsonResponse(
            {"error": "Unknown mood"},
            status=400
        )

    tracks = list(
        queryset.values(
            "track_name",
            "artist_name",
            "genre",
            "energy",
            "danceability",
            "acousticness"
        )[:]
    )

    return JsonResponse({
        "mood": mood,
        "count": len(tracks),
        "tracks": tracks
    })

##################################################################################################################################

def track_list_api(request):
    tracks = Track.objects.all().values(
        "id",
        "track_name",
        "artist_name",
        "genre",
        "popularity",
        "danceability",
        "energy",
        "acousticness",
        "instrumentalness",
        "duration_ms"
    )
    return JsonResponse(list(tracks), safe=False)
    