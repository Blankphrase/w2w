import json
import unittest
from unittest.mock import patch

from django.test import TestCase

from tmdb.client import Client
from tmdb.models import (
    Movie, MoviePopularQuery, NowPlayingQuery,
    MIN_UPDATE_LEVEL, MAX_UPDATE_LEVEL
)
from tmdb.util import tmdb_request


class NowPlayingTest(TestCase):

    def setUp(self):
        self.tmdb_client = Client()

        for i in range(5):
            Movie.objects.create(
                id = i, title = "movie %d" % i, update_level = 100
            )
        npq = NowPlayingQuery.objects.create(
            page = 1, total_pages = 2, total_results = 4
        )
        npq.movies.add(Movie.objects.get(id = 0))
        npq.movies.add(Movie.objects.get(id = 1))

        npq = NowPlayingQuery.objects.create(
            page = 2, total_pages = 2, total_results = 4
        )
        npq.movies.add(Movie.objects.get(id = 2))
        npq.movies.add(Movie.objects.get(id = 3))
       
    def tearDown(self):
        Movie.objects.all().delete()
        NowPlayingQuery.objects.all().delete()

    def test_returns_list_with_movies(self):
        data = self.tmdb_client.get_nowplaying_movies(page = 1)
        movies_id = set(movie["id"] for movie in data["movies"])
        self.assertEqual(movies_id, set([0, 1]))

    def test_returns_proper_page(self):
        data = self.tmdb_client.get_nowplaying_movies(page = 2)
        self.assertEqual(data["page"], 2)

    @patch("tmdb.models.tmdb_request")
    def test_returns_empty_list_for_out_of_range_page(self, tmdb_mock):
        tmdb_mock.return_value = {
            "page":3,"results":[],
            "total_pages":2,"total_results": 4
        }
        data = self.tmdb_client.get_nowplaying_movies(page = 3)
        self.assertEqual(len(data["movies"]), 0)


class PopularMoviesTest(TestCase):

    def setUp(self):
        self.tmdb_client = Client()

        for i in range(5):
            Movie.objects.create(
                id = i, title = "movie %d" % i, update_level = 100
            )
        npq = MoviePopularQuery.objects.create(
            page = 1, total_pages = 2, total_results = 4
        )
        npq.movies.add(Movie.objects.get(id = 0))
        npq.movies.add(Movie.objects.get(id = 1))

        npq = MoviePopularQuery.objects.create(
            page = 2, total_pages = 2, total_results = 4
        )
        npq.movies.add(Movie.objects.get(id = 2))
        npq.movies.add(Movie.objects.get(id = 3))
       
    def tearDown(self):
        Movie.objects.all().delete()
        MoviePopularQuery.objects.all().delete()

    def test_returns_list_with_movies(self):
        data = self.tmdb_client.get_popular_movies(page = 1)
        movies_id = set(movie["id"] for movie in data["movies"])
        self.assertEqual(movies_id, set([0, 1]))

    def test_returns_proper_page(self):
        data = self.tmdb_client.get_popular_movies(page = 2)
        self.assertEqual(data["page"], 2)

    @patch("tmdb.models.tmdb_request")
    def test_returns_empty_list_for_out_of_range_page(self, tmdb_mock):
        tmdb_mock.return_value = {
            "page":3,"results":[],
            "total_pages":2,"total_results": 4
        }
        data = self.tmdb_client.get_popular_movies(page = 3)
        self.assertEqual(len(data["movies"]), 0)


class ClientSearchTest(TestCase):

    def setUp(self):
        self.tmdb_client = Client()
        self.request_response = {
            "results": [ 
                {"title": "0940", "id": 9}, 
                {"title": "RGui", "id": 41} 
            ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }

    @patch("tmdb.client.tmdb_request")
    def test_call_search_with_proper_arguments(self, tmdb_mock):
        query = "Terminator"
        response = self.tmdb_client.search_movies(query = query, page = 1)
        tmdb_mock.assert_called_once_with(method = "POST", 
            path = "search/movie", params = {"page": 1, "query": query})

    @patch("requests.request")
    def test_get_searching_results(self, request_mock):
        request_mock.return_value.json.return_value = self.request_response
        response = self.tmdb_client.search_movies(query = "terminator", page=1)
        self.assertEqual(response["total_results"], 2)
        self.assertEqual(len(response["movies"]), 2)

    @patch("requests.request")
    def test_save_search_movies_in_database(self, request_mock):
        request_mock.return_value.json.return_value = self.request_response
        self.tmdb_client.search_movies(query = "terminator", page=1)        
        self.assertEqual(Movie.objects.count(), 2)

    @patch("requests.request")
    def test_search_empty_query(self, request_mock):
        request_mock.return_value.json.return_value = {
            "page":1,"results":[],"total_pages":1,"total_results":0
        }
        response = self.tmdb_client.search_movies(query = "sdfsdfsfsdf", page=1)  
        self.assertEqual(response["total_results"], 0)
        self.assertEqual(response["page"], 1)

    @patch("requests.request")
    def test_search_for_no_matching_query(self, request_mock):
        request_mock.return_value.json.return_value = {
            "page":1,"results":[],"total_results":0,"total_pages":1
        }
        response = self.tmdb_client.search_movies(query = "sdfsdfsfsdf", page=1)  
        self.assertEqual(response["total_results"], 0)
        self.assertEqual(response["page"], 1)