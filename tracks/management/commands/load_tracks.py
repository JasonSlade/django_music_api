import csv
from django.core.management.base import BaseCommand
from tracks.serializers import TrackSerializer
from pathlib import Path

MAX_ROWS = 9500

class Command(BaseCommand):
    help = "Load the 9500 tracks from CSV into database"

    def handle(self, *args, **kwargs):
        # relative path in file
        csv_path = Path("SpotifyFeatures.csv")
        # check file exists
        if not csv_path.exists():
            self.stderr.write("CSV file not found.")
            return

        count = 0
        # open + read csv file
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # go over each row
            for row in reader:
                if count >= MAX_ROWS:
                    break
                
                # use drf serialiser for validatin + saving
                #serializer = TrackSerializer(data=row)
                clean_row = {}
                # ensure genre is included
                for key, value in row.items():
                    clean_key = key.replace("\ufeff", "").strip()
                    clean_row[clean_key] = value

                serializer = TrackSerializer(data=clean_row)


                if serializer.is_valid():
                    serializer.save()
                    count += 1
                else:
                    self.stderr.write(
                        f"Invalid row skipped: {serializer.errors}"
                    )

      
