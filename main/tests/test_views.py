from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import PrefList
from reco.models import Reco
from reco.engine import RecoManager
from tmdb.models import Movie

from unittest.mock import Mock, patch
import json


User = get_user_model()


class HomePageTest(TestCase):

    def test_show_homepage_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')


class RecoPageTest(TestCase):

    def setUp(self):
        self.reco_output = [
            { "id": 1, "freq": 100, "rating": 10}, 
            { "id": 2, "freq": 200, "rating": 9 },
            { "id": 5, "freq": 100, "rating": 1 }
        ]
        self.prefs = [
            { "id": 3, "rating": 10 },
            { "id": 4, "rating": 1 }
        ]

        for i in range(1, 6):
            Movie.objects.create(id = i, title = "movie_%d" % i)


    def tearDown(self):
        Movie.objects.all().delete()


    def test_use_reco_template(self):
        response = self.client.get("/reco")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/reco.html")


    @patch("main.views.RecoManager")
    def test_make_reco_returns_json_with_movies(self, rmanager_mock):
        rmanager_mock.return_value.make_reco.return_value = self.reco_output

        response = self.client.post("/make_reco", 
            json.dumps({
                "type": "standalone",
                "prefs": self.prefs
            }),
            content_type="application/json"
        )
        reco_movies = json.loads(response.content.decode())["movies"]
        reco_movies_id = [ movie["id"] for movie in reco_movies ]

        self.assertTrue(1 in reco_movies_id)
        self.assertTrue(2 in reco_movies_id)
        self.assertFalse(3 in reco_movies_id)


    @patch("main.views.RecoManager")
    def test_make_reco_creates_preflist_for_anonymous_user(self, rmanager_mock):
        rmanager_mock.return_value.make_reco.return_value = self.reco_output

        response = self.client.post("/make_reco", 
            json.dumps({
                "type": "standalone",
                "prefs": self.prefs
            }),
            content_type="application/json"
        )
        self.assertEqual(PrefList.objects.count(), 1)
        self.assertIsNone(PrefList.objects.first().user)


    @patch("main.views.SlopeOne")
    def test_make_reco_creates_reco_obj_for_auth_users(self, engine_mock):
        engine_mock.return_value.make_reco.return_value = self.reco_output

        user = User(email = "test@jago.com")
        user.set_password("test")
        user.save()

        is_logged = self.client.login(email = "test@jago.com", password = "test")
        self.assertTrue(is_logged)

        response = self.client.post("/make_reco", 
            json.dumps({
                "type": "standalone",
                "prefs": self.prefs
            }),
            content_type="application/json"
        )
        
        self.assertEqual(Reco.objects.count(), 1)
        self.assertEqual(Reco.objects.first().user, user)



    @patch("main.views.SlopeOne")
    def test_make_reco_creates_reco_obj_with_selected_movies(self, engine_mock):
        engine_mock.return_value.make_reco.return_value = self.reco_output

        response = self.client.post("/make_reco", 
            json.dumps({
                "type": "standalone",
                "prefs": self.prefs
            }),
            content_type="application/json"
        )
        
        # There are three movies that should be return by engine, but
        # view modify the list by removing the movies with ratings
        # below given threshold. In this test view should show 2 movies.
        self.assertEqual(Reco.objects.first().movies.count(), 2)

