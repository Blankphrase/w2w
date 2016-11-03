from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import PrefList
from reco.models import Reco
from reco.engine import RecoManager
from tmdb.models import Movie

from unittest.mock import Mock, patch
import json


User = get_user_model()


class AboutTest(TestCase):

    def test_for_using_about_template(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/about.html")


class HomePageTest(TestCase):

    def create_and_login_user(self, email = "test@jago.com", password="test"):
        user = User(email = email)
        user.set_password(password)
        user.save()
        self.client.login(email = "test@jago.com", password = "test")
        return user

    def test_show_homepage_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_for_passing_reco_to_template(self):
        user = self.create_and_login_user()
        reco = Reco.objects.create(user = user, title = "Reco #1")
        response = self.client.get("/")
        self.assertIsInstance(response.context["reco"], Reco)
        self.assertEqual(response.context["reco"].title, reco.title)

    def test_for_none_reco_if_anonymous_user(self):
        response = self.client.get("/")
        self.assertIsNone(response.context["reco"])

    def test_for_none_reco_if_no_previous_recos(self):
        user = self.create_and_login_user()
        response = self.client.get("/")
        self.assertIsNone(response.context["reco"])


class RecoTest(TestCase):

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


    def create_and_login_user(self, email = "test@jago.com", password="test"):
        user = User(email = email)
        user.set_password(password)
        user.save()

        self.client.login(email = "test@jago.com", password = "test")

        return user
       

    def test_use_reco_template(self):
        response = self.client.get("/reco")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/reco.html")


    def test_for_passing_movies_to_template(self):
        user = self.create_and_login_user()
        user.add_pref(3, 10)
        user.add_pref(4, 1)

        response = self.client.get("/reco", {"type": "general"})
        self.assertEqual(len(response.context["preflist"]), 2)


    def test_for_capturing_reco_type_from_get_args__standalone(self):
        user = self.create_and_login_user()
        user.add_pref(3, 10)
        user.add_pref(4, 1)

        response = self.client.get("/reco", {"type": "standalone"})
        self.assertEqual(len(response.context["preflist"]), 0)

    def test_for_capturing_reco_type_from_get_args__general(self):
        user = self.create_and_login_user()
        user.add_pref(3, 10)
        user.add_pref(4, 1)

        response = self.client.get("/reco", {"type": "general"})
        self.assertEqual(len(response.context["preflist"]), 2)


    def test_for_passing_empty_movies_list_to_template_for_anonym_users(self):
        response = self.client.get("/reco")
        self.assertEqual(response.context["preflist"], [])


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