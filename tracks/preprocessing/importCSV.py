import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_api.settings")
django.setup()

from tracks.models import Track

CSV_PATH = "/Users/jasonslade/Desktop/django_music_api/Tracks.csv"

def run():
    print("Loading CSV from:", CSV_PATH)


    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        print("Detected columns:", reader.fieldnames)

        Track.objects.all().delete()

        tracks = []
        for row in reader:
            tracks.append(Track(
                genre=row.get("genre") or row.get("\ufeffgenre"),
                artist_name=row["artist_name"],
                track_name=row["track_name"],
                track_id=row["track_id"],
                popularity=int(row["popularity"]),
                acousticness=float(row["acousticness"]),
                danceability=float(row["danceability"]),
                duration_ms=int(row["duration_ms"]),
                energy=float(row["energy"]),
                instrumentalness=float(row["instrumentalness"]),
            ))

        Track.objects.bulk_create(tracks)

    print(f"Imported {len(tracks)} rows into SQLite.")

if __name__ == "__main__":
    run()
