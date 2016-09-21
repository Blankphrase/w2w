from tmdb.models import Movie
from reco.models import Reco

from django.test import TestCase
from django.contrib.auth import get_user_model

import unittest
from unittest.mock import Mock, patch


User = get_user_model()


class RecoModelTest(TestCase):

    def setUp(self):
        self.preferences = [
            { "title": "Killer", "id": 10, "rating": 8 },
            { "title": "Spiderman", "id": 19, "rating": 6 },
            { "title": "Terminator 2", "id": 5, "rating": 10 }
        ]
        self.reco = [
            { "title": "Killer 2", "id": 11},
            { "title": "Batman Begins", "id": 100 },
            { "title": "Terminator", "id": 50 }
        ]

        for movie in self.preferences:
            Movie.objects.create(title = movie["title"], id = movie["id"])
        for movie in self.reco:
            Movie.objects.create(title = movie["title"], id = movie["id"])

    def tearDown(self):
        Movie.objects.all().delete()
        Reco.objects.all().delete()

    def test_create_new_creates_reco(self):
        Reco.create_new(
            base = self.preferences, 
            reco = self.reco, 
            user = None
        )        
        self.assertEqual(Reco.objects.count(), 1)

    def test_create_new_links_base_movies_to_reco(self):
        reco = Reco.create_new(
            base = self.preferences, 
            reco = self.reco, 
            user = None
        )  
        self.assertEqual(reco.base.count(), 3)
        self.assertTrue(reco.base.filter(id=self.preferences[0]["id"]).exists())
        self.assertTrue(reco.base.filter(id=self.preferences[1]["id"]).exists())
        self.assertTrue(reco.base.filter(id=self.preferences[2]["id"]).exists())
        self.assertFalse(reco.base.filter(id=self.reco[2]["id"]).exists())

    def test_create_new_links_reco_movies_to_reco(self):
        reco = Reco.create_new(
            base = self.preferences, 
            reco = self.reco, 
            user = None
        )      
        self.assertEqual(reco.movies.count(), 3)
        self.assertTrue(reco.movies.filter(id=self.reco[0]["id"]).exists())
        self.assertTrue(reco.movies.filter(id=self.reco[1]["id"]).exists())
        self.assertTrue(reco.movies.filter(id=self.reco[2]["id"]).exists())
        self.assertFalse(reco.movies.filter(id=self.preferences[2]["id"]).exists())

    def test_create_new_links_user_to_reco(self):
        user = User.objects.create()
        reco = Reco.create_new(
            base = self.preferences, 
            reco = self.reco, 
            user = user
        )    
        self.assertEqual(user.reco_set.count(), 1)