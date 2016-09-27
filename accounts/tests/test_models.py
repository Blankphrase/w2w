from tmdb.models import Movie
from accounts.models import MoviePref, PrefList

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):
        self.pref = [
            { "title": "Killer", "id": 10, "rating": 8 },
            { "title": "Spiderman", "id": 19, "rating": 6 },
            { "title": "Terminator 2", "id": 5, "rating": 10 }
        ]
        for movie in self.pref:
            Movie.objects.create(title = movie["title"], id = movie["id"])


    def test_user_is_authenticated(self):
        user = User()
        self.assertTrue(user.is_authenticated)


    def test_user_has_no_username(self):
        user = User()
        self.assertFalse(hasattr(user, "username"))


    def tset_user_has_email(self):
        user = User()
        self.assertTrue(hasattr(user, "email"))


    def test_user_requires_email(self):
        user = User(password = "test")
        with self.assertRaises(ValidationError):
             user.full_clean()


    def test_user_clean_with_email(self):
        user = User(email = "admin@jago.com", password = "test")
        user.full_clean()


    def test_user_has_pref_list_by_default(self):
        user = User.objects.create(email = "admin@jago.com", password = "test")
        self.assertEqual(user.pref, PrefList.objects.first())
        

    def test_add_prev_links_user_to_movie(self):
        user = User.objects.create()
        user.add_pref(id = self.pref[0]["id"], rating = self.pref[0]["rating"]) 
        self.assertEqual(MoviePref.objects.count(), 1)
        self.assertEqual(self.pref[0]["id"], user.pref.movies.first().id)


    def test_add_prev_raises_error_when_movie_not_in_db(self):
        user = User.objects.create()    
        with self.assertRaises(Movie.DoesNotExist):
            user.add_pref(id = 1323, rating = 10)
        

    def test_add_prev_updates_pref_when_set(self):
        user = User.objects.create()
        user.add_pref(id = self.pref[0]["id"], rating = 1)
        user.add_pref(id = self.pref[0]["id"], rating = 2)
        self.assertEqual(user.pref.movies.count(), 1)
        self.assertEqual(user.pref.data.first().rating, 2)


    def test_add_prev_sets_rating_to_10_by_default(self):
        user = User.objects.create()
        user.add_pref(id = self.pref[0]["id"])
        self.assertEqual(
            user.pref.data.get(movie__id=self.pref[0]["id"]).rating, 
            10
        )


    def test_get_pref_returns_preferences_for_given_id(self):
        user = User.objects.create()
        movie_id = self.pref[0]["id"]
        user.add_pref(id = movie_id, rating = 9)
        self.assertEqual(user.get_pref(movie_id).rating, 9)


    def test_get_pref_raises_error_when_pref_does_not_exist(self):
        user = User.objects.create()
        with self.assertRaises(MoviePref.DoesNotExist):
            user.get_pref(10)       


    def test_remove_pref(self):
        user = User.objects.create()
        movie_id = self.pref[0]["id"]
        user.add_pref(id = movie_id, rating = 9)
        self.assertEqual(user.pref.data.count(), 1)
        user.remove_pref(id = movie_id)
        self.assertEqual(user.pref.data.count(), 0)