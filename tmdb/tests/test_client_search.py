from django.test import TestCase

from tmdb.client import Client
from tmdb.models import Movie, MoviePopularQuery
from tmdb.util import tmdb_request

import json
from unittest.mock import patch
from unittest import skip


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
            "errors": ["query must be provided"]
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

