# we will be refrencing: https://docs.djangoproject.com/en/6.0/topics/testing/overview/ + 
# https://www.geeksforgeeks.org/python/how-to-add-unit-testing-to-django-project/ for this part of the project.



import json
from django.test import TestCase
from tracks.models import Track


# Create your tests here.

# To run tests: python3 manage.py test tracks

#######################################################################################################################################



class TrackAPITests(TestCase):
    # creates a test track to run our tests on
    def setUp(self):
        self.track = Track.objects.create(
            genre="Pop",
            artist_name="Test Artist",
            track_name="Test Track",
            popularity=75,
            acousticness=0.3,
            danceability=0.7,
            duration_ms=200000,
            energy=0.8,
            instrumentalness=0.1,
        )

    # 1. create track
    # we test: does POST /api/tracks/create/ create a track and return 201
    # checks does "CREATE" do what it should do
    # sends a POST request to create endpoint view calls Track.objects.create(...),
    # the test then verifies that a new database row exists.
    def test_create_track_api(self):
        response = self.client.post(
            "/api/tracks/create/",
            data=json.dumps({
                "genre": "Rock",
                "artist_name": "New Artist",
                "track_name": "New Track",
                "popularity": 60,
                "acousticness": 0.2,
                "danceability": 0.5,
                "duration_ms": 180000,
                "energy": 0.6,
                "instrumentalness": 0.0,
            }),
            content_type="application/json"
        )
        # if track not created test would fail
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Track.objects.filter(track_name="New Track").exists()
        )

    # 2. delete track
    # we test: does DELETE /api/tracks/<id>/ remove the track
    # checks does "DELETE" do what it should do
    # use an existing track + send delete request - verify track is gone
    def test_delete_track_api(self):
        response = self.client.delete(
            f"/api/tracks/{self.track.id}/"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Track.objects.filter(id=self.track.id).exists()
        )

    # 3. search track
    # we test: if the search filtering works correctly
    # checks does "SEARCH" return what it should do
    # send GET with parameters
    def test_search_tracks_api(self):
        response = self.client.get(
            "/api/tracks/search/",
            {"artist_name": "Test"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["track_name"], "Test Track")

    # 4. get track by id
    # we test: does GET /api/track/<id>/ return correct track
    def test_get_track_api(self):
        response = self.client.get(
            f"/api/track/{self.track.id}/"
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["track_name"], "Test Track")
        self.assertEqual(data["artist_name"], "Test Artist")

    # 5. update track
    # we test: find the correct track by ID and changes are added to database
    def test_update_track_api(self):
        response = self.client.post(
            f"/api/track/{self.track.id}/update/",
            data=json.dumps({
                "track_name": "Updated Track",
                "popularity": 90
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        self.track.refresh_from_db()
        self.assertEqual(self.track.track_name, "Updated Track")
        self.assertEqual(self.track.popularity, 90)

    # 6. genre avg
    # we test: does the genre exist, does aggregation occur and do we recieve a response in the correct format
    def test_genre_averages_api(self):
        response = self.client.get(
            "/api/genres/Pop/averages/"
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["genre"], "Pop")
        self.assertIn("averages", data)
        self.assertIn("energy", data["averages"])

    # 7. mood test
    # tests endpoint exists and responds successfully
    def test_mood_happy_api_endpoint_exists(self):
        response = self.client.get("/api/moods/happy/")

        # endpoint exists and responds
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # response has expected top level key
        self.assertIn("tracks", data)

        # tracks should be a list
        self.assertIsInstance(data["tracks"], list)
