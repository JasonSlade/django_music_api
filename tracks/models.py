from django.db import models

# Create your models here.

# Add defaults for numeric fields
# Track model to represent a spotify music track
class Track(models.Model):
    # base identifiers
    genre = models.CharField(max_length=100, default="")
    artist_name = models.CharField(max_length=255, default="")
    track_name = models.CharField(max_length=255, default="")
    track_id = models.CharField(max_length=64)

    # ratings
    popularity = models.PositiveSmallIntegerField(default=0, help_text="0-100")
    acousticness = models.FloatField(default=0.0)
    danceability = models.FloatField(default=0.0)

    # duration
    duration_ms = models.PositiveIntegerField(default=0, help_text="Duration in milliseconds")

    # audio features
    energy = models.FloatField(default=0.0)
    instrumentalness = models.FloatField(default=0.0)
