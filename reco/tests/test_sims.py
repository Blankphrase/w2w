from django.test import TestCase
from django.contrib.auth import get_user_model

from tmdb.models import Movie
from reco.source import UserSource
from accounts.models import MoviePref, PrefList
from reco.sims import cos_sim, cos_sim_adjusted


User = get_user_model()


class SimsTest(TestCase):

    def setUp(self):
        # create sample dataset
        self.movies = dict()
        for i in range(1, 6):
            self.movies[i] = Movie.objects.create(id = i, title = "movie%d" % i)
        self.users = dict()
        for i in range(1, 5):
            self.users[i] = User.objects.create(email = "user%d" % i,
                password = "user")
        self.users["Alice"] = User.objects.create(email = "Alice",
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
        self.users[3].add_pref(id=1, rating=3)
        self.users[3].add_pref(id=2, rating=3)
        self.users[3].add_pref(id=3, rating=1)
        self.users[3].add_pref(id=4, rating=5)
        self.users[3].add_pref(id=5, rating=4)
        self.users[4].add_pref(id=1, rating=1)
        self.users[4].add_pref(id=2, rating=5)
        self.users[4].add_pref(id=3, rating=5)
        self.users[4].add_pref(id=4, rating=2)
        self.users[4].add_pref(id=5, rating=1)
        self.users["Alice"].add_pref(id=1, rating=5)
        self.users["Alice"].add_pref(id=2, rating=3)
        self.users["Alice"].add_pref(id=3, rating=4)
        self.users["Alice"].add_pref(id=4, rating=4)

        self.source = UserSource(self.users["Alice"])

    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        MoviePref.objects.all().delete()
        PrefList.objects.all().delete()

    def test_calc_similarity_between_two_movies(self):
        movies_sim = cos_sim(
            Movie.objects.get(id = 1),
            Movie.objects.get(id = 5)
        )
        self.assertAlmostEqual(movies_sim, 0.994, 3)

    def test_calc_similarity_adjusted_between_two_movies(self):
        movies_sim = cos_sim_adjusted(
            Movie.objects.get(id = 1),
            Movie.objects.get(id = 5)
        )
        self.assertAlmostEqual(movies_sim, 0.80, 2)