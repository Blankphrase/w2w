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


    @patch("tmdb.client.tmdb_request")
    def test_call_search_with_proper_arguments(self, tmdb_mock):
        query = "Terminator"
        response = self.tmdb_client.search_movies(query = query, page = 1)
        tmdb_mock.assert_called_once_with(method = "POST", 
            path = "search/movie", params = {"page": 1, "query": query})

    @patch("requests.request")
    def test_get_searching_results(self):
        request_mock.return_value.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }
        response = self.tmdb_client.search_movies(query = "terminator", page=1)


    def test_save_search_movies_in_database(self):
        pass

    def test_search_empty_query(self):
        pass


