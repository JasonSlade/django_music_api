# this is the serializer we will use for each row of CSV

from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = [
            'id',
            'genre',
            'artist_name',
            'track_name',
            'track_id',
            'popularity',
            'acousticness',
            'danceability',
            'duration_ms',
            'energy',
            'instrumentalness'
        ]
