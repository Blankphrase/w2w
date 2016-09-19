from reco.engine import RecoManager, Item2Item
from reco.exceptions import RecoSourceError
from reco.source import JsonSource, UserSource
from reco.models import Reco
from tmdb.models import Movie
from accounts.models import MoviePref, PrefList

from django.contrib.auth import get_user_model
from django.test import TestCase

import unittest
from unittest.mock import Mock, patch


User = get_user_model()


class RecoManagerTest(unittest.TestCase):
    '''
    RecoManager uses Source (UserSource or JsonSource) as source for user
    preferences. Source is an abstract class, which unfortunatley cannont
    be initialised and in turn cannot be mock out. In turn, one of the 
    derived class needs to be used. UserSource has been chosen.
    '''

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
        self.source = JsonSource(self.preferences)

    def tearDown(self):
        Movie.objects.all().delete()
        User.objects.all().delete()
        MoviePref.objects.all().delete()
        PrefList.objects.all().delete()
        
    def test_creates_base_for_reco_in_constructor(
        self
    ):
        rengine = RecoManager(self.source)
        self.assertEqual(rengine.base, self.preferences)

    def test_raises_error_when_source_is_empty(
        self
    ):
        rengine = RecoManager(JsonSource([]))
        with self.assertRaises(RecoSourceError):
            rengine.get_reco()

    @patch("reco.engine.Reco")
    def test_get_reco_accepts_user_as_argument(
        self, mock_reco
    ):
        mock_create = Mock()
        mock_reco.create_new = mock_create

        RecoManager(self.source).get_reco(User.objects.create())

    @patch("reco.engine.Reco")
    def test_get_reco_accepts_none_user(
        self, mock_reco
    ):
        mock_create = Mock()
        mock_reco.create_new = mock_create

        RecoManager(self.source).get_reco()

    @patch("reco.engine.Reco")
    @patch("reco.engine.Item2Item")
    def test_get_reco_calls_create_new_with_base_and_reco(
        self, mock_engine, mock_reco
    ):
        mock_create = Mock()
        mock_reco.create_new = mock_create
        mock_engine.return_value.make_reco.return_value = self.reco

        RecoManager(self.source).get_reco()

        mock_create.assert_called_once_with(
            base = self.preferences,
            reco = self.reco,
            user = None
        )

    @patch("reco.engine.Item2Item")
    def test_get_reco_returns_reco_object(
        self, mock_engine
    ):
        mock_engine.return_value.make_reco.return_value = self.reco
        for movie in self.reco + self.preferences:
            Movie.objects.create(id = movie["id"], title = movie["title"])

        reco = RecoManager(self.source).get_reco()
        reco_db = Reco.objects.first()
        self.assertEqual(reco, reco_db)


    @patch("reco.engine.Item2Item")
    def test_make_reco_returns_list_of_movies_dict(
        self, mock_engine
    ):
        mock_engine.return_value.make_reco.return_value = self.reco

        reco = RecoManager(self.source).make_reco()
        self.assertEqual(reco, self.reco)