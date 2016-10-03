from django.test import TestCase

from tmdb.client import Client
from tmdb.models import (
    Movie, MoviePopularQuery,
    MIN_UPDATE_LEVEL, MAX_UPDATE_LEVEL
)
from tmdb.exceptions import MovieDoesNotExist
from tmdb.util import tmdb_request

import json
import unittest
from unittest.mock import patch


@patch("requests.request")
class ClientTest(TestCase):

    def setUp(self):
        self.tmdb_client = Client()

        self.response_id_550 = {
            "adult":False,"backdrop_path":"/8uO0gUM8aNqYLs1OsTBQiXu0fEv.jpg",
            "belongs_to_collection":None,
            "budget":63000000, "genres":[{"id":18,"name":"Drama"}],
            "homepage":"http://www.foxmovies.com/movies/fight-club",
            "id":550,"imdb_id":"tt0137523",
            "original_language":"en","original_title":"Fight Club",
            "overview":"A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an out-of-control spiral toward oblivion.",
            "popularity":3.969124,
            "poster_path":"/811DjJTon9gD6hZ8nCjSitaIXFQ.jpg",
            "production_companies":[
                {"name":"Regency Enterprises","id":508},
                {"name":"Fox 2000 Pictures","id":711},
                {"name":"Taurus Film","id":20555},
                {"name":"Linson Films","id":54050},
                {"name":"Atman Entertainment","id":54051},
                {"name":"Knickerbocker Films","id":54052}
            ], "production_countries":[
                {"iso_3166_1":"DE","name":"Germany"},
                {"iso_3166_1":"US","name":"United States of America"}
            ],"release_date":"1999-10-14","revenue":100853753,"runtime":139,
            "spoken_languages":[
                {"iso_639_1":"en","name":"English"}],
            "status":"Released",
            "tagline":"How much can you know about yourself if you've never been in a fight?",
            "title":"Fight Club","video":False,
            "vote_average":8.1,"vote_count":5385}
    

    def test_get_movie_send_request_if_movie_not_in_db(self, request_mock):
        request_mock.return_value.json.return_value = self.response_id_550
        self.tmdb_client.get_movie(id = 550)
        self.assertTrue(request_mock.called)


    def test_get_movie_does_not_send_request_if_movie_in_db(
        self, request_mock
    ):
        request_mock.return_value.json.return_value = self.response_id_550
        movie = self.tmdb_client.get_movie(id = 550)
        self.tmdb_client.get_movie(id = 550)
        self.assertEqual(request_mock.call_count, 1)


    def test_get_movie_sends_request_when_update_level_too_low(
        self, request_mock
    ):
        request_mock.return_value.json.return_value = self.response_id_550
        movie = self.tmdb_client.get_movie(id = 550)
        movie.update_level = MIN_UPDATE_LEVEL
        movie.save()
        self.tmdb_client.get_movie(id = 550, min_update_level = 2)
        self.assertEqual(request_mock.call_count, 2)


    def test_get_movie_returns_Movie_object(self, request_mock):
        request_mock.return_value.json.return_value = self.response_id_550
        movie = self.tmdb_client.get_movie(id = 550)
        self.assertIsInstance(movie, Movie)


    def test_get_movie_sets_highest_update_level(self, request_mock):
        request_mock.return_value.json.return_value = self.response_id_550
        movie = self.tmdb_client.get_movie(id = 550)
        self.assertEqual(movie.update_level, MAX_UPDATE_LEVEL)


    def test_get_movie_saves_movie_in_database(self, request_mock):
        request_mock.return_value.json.return_value = self.response_id_550
        self.tmdb_client.get_movie(id = 550)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.first().title, 
            self.response_id_550["title"])


    def test_get_movie_raises_MovieDoesNotExist_exception(self, request_mock):
        request_mock.return_value.json.return_value = {
            "status_code": 34,
            "status_message":"The resource you requested could not be found."
        }
        with self.assertRaises(MovieDoesNotExist):
            self.tmdb_client.get_movie(id = 5345)