from reco.source import UserSource
from tmdb.models import Movie 
from accounts.models import MoviePref, PrefList

from django.contrib.auth import get_user_model

import unittest
from unittest.mock import Mock, patch


User = get_user_model()


class UserSourceTest(unittest.TestCase):

    def setUp(self):
        # create sample dataset
        self.movies = dict()
        for i in range(1, 6):
            self.movies[i] = Movie.objects.create(id = i, title = "movie%d" % i)
        self.users = dict()
        for i in range(1, 4):
            self.users[i] = User.objects.create(email = "user%d" % i,
                password = "user")

        self.users[1].add_pref(id=1, rating=3)
        self.users[1].add_pref(id=2, rating=1)
        self.users[1].add_pref(id=3, rating=2)
        self.users[1].add_pref(id=4, rating=3)
        self.users[1].add_pref(id=5, rating=3)
        self.users[2].add_pref(id=1, rating=4)
        self.users[2].add_pref(id=2, rating=3)
        self.users[2].add_pref(id=3, rating=4)
        self.users[2].add_pref(id=4, rating=3)
        self.users[2].add_pref(id=5, rating=5)

    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        MoviePref.objects.all().delete()
        PrefList.objects.all().delete()

    def test_get_data_returns_dict(self):
        self.source = UserSource(self.users[1])
        data = [
            { "id": 1, "rating": 3},
            { "id": 2, "rating": 1},
            { "id": 3, "rating": 2},
            { "id": 4, "rating": 3},
            { "id": 5, "rating": 3}
        ]
        self.assertEqual(self.source.get_data(), data)

    def test_is_empty_true_when_no_favouritve_movies(self):
        self.source = UserSource(self.users[3])
        self.assertTrue(self.source.is_empty())

    def test_is_empty_false_when_favourite_movies(self):
        self.source = UserSource(self.users[2])
        self.assertFalse(self.source.is_empty())