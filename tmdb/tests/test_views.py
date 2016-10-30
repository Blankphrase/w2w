import json
from unittest.mock import patch, ANY

from django.test import TestCase

from tmdb.client import Client
from tmdb.models import Movie, MoviePopularQuery
from django.http.response import JsonResponse


@patch("tmdb.views.Client.get_movie")
class MovieInfoTest(TestCase):

    def setUp(self):
        pass

    def test_returns_json_response(self, mock_client):
        response = self.client.get("/movies/%d/info" % 550)
        self.assertIsInstance(response, JsonResponse)

    def test_calls_client_with_the_proper_id(self, mock_client):
        self.client.get("/movies/%d/info" % 550)
        mock_client.assert_called_with(id = 550, min_update_level = ANY)


@patch("tmdb.views.Client.get_nowplaying_movies")
class NowPlayingTest(TestCase):

    def setUp(self):
        self.mock_response = {
            "results": [ 
                {"title": "Figt Club", "id": 550}, 
                {"title": "Matrix", "id": 41} 
            ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }

    def test_returns_json_response(self, mock_client):
        mock_client.return_value = self.mock_response
        response = self.client.get("/movies/nowplaying")
        self.assertIsInstance(response, JsonResponse)

    def test_returns_movies_in_response(self, mock_client):
        mock_client.return_value = self.mock_response
        response = self.client.get("/movies/nowplaying", data={"page": 1})
        data = json.loads(response.content.decode())
        self.assertEqual(data["total_results"], 2)

    def test_calls_tmdb_client_method(self, mock_client):
        mock_client.return_value = self.mock_response
        self.client.get("/movies/nowplaying")
        self.assertTrue(mock_client.called)

    def test_calls_tmdb_client_with_proper_page(self, mock_client):
        mock_client.return_value = self.mock_response
        self.client.get("/movies/nowplaying", data={"page": 4})
        mock_client.assert_called_with(page = 4)
    


@patch("tmdb.views.Client.get_upcoming_movies")
class UpcomingTest(TestCase):

    def setUp(self):
        self.mock_response = {
            "results": [ 
                {"title": "Figt Club", "id": 550}, 
                {"title": "Matrix", "id": 41} 
            ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }

    def test_returns_json_response(self, mock_client):
        mock_client.return_value = self.mock_response
        response = self.client.get("/movies/upcoming")
        self.assertIsInstance(response, JsonResponse)

    def test_returns_movies_in_response(self, mock_client):
        mock_client.return_value = self.mock_response
        response = self.client.get("/movies/upcoming", data={"page": 1})
        data = json.loads(response.content.decode())
        self.assertEqual(data["total_results"], 2)

    def test_calls_tmdb_client_method(self, mock_client):
        mock_client.return_value = self.mock_response
        self.client.get("/movies/upcoming")
        self.assertTrue(mock_client.called)

    def test_calls_tmdb_client_with_proper_page(self, mock_client):
        mock_client.return_value = self.mock_response
        self.client.get("/movies/upcoming", data={"page": 4})
        mock_client.assert_called_with(page = 4)
    

@patch("tmdb.views.Client.get_toprated_movies")
class TopRatedTest(TestCase):

    def setUp(self):
        self.mock_response = {
            "results": [ 
                {"title": "Figt Club", "id": 550}, 
                {"title": "Matrix", "id": 41} 
            ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }

    def test_returns_json_response(self, mock_client):
        mock_client.return_value = self.mock_response
        response = self.client.get("/movies/toprated")
        self.assertIsInstance(response, JsonResponse)

    def test_returns_movies_in_response(self, mock_client):
        mock_client.return_value = self.mock_response
        response = self.client.get("/movies/toprated", data={"page": 1})
        data = json.loads(response.content.decode())
        self.assertEqual(data["total_results"], 2)

    def test_calls_tmdb_client_method(self, mock_client):
        mock_client.return_value = self.mock_response
        self.client.get("/movies/toprated")
        self.assertTrue(mock_client.called)

    def test_calls_tmdb_client_with_proper_page(self, mock_client):
        mock_client.return_value = self.mock_response
        self.client.get("/movies/toprated", data={"page": 4})
        mock_client.assert_called_with(page = 4)
    

@patch("tmdb.views.Client.search_movies")
class SearchMoviesTest(TestCase):

    def setUp(self):
        self.mock_response = {
            "results": [ 
                {"title": "Figt Club", "id": 550}, 
                {"title": "Matrix", "id": 41} 
            ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }


    def test_returns_json_response(self, mock_client):
        mock_client.return_value = self.mock_response
        response = self.client.get(
            "/movies/search", 
            data={"query": "terminator", "page": 4}
        )
        self.assertIsInstance(response, JsonResponse)

    def test_returns_movies_in_response(self, mock_client):
        mock_client.return_value = self.mock_response
        response = self.client.get(
            "/movies/search", 
            data={"query": "terminator", "page": 4}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(data["total_results"], 2)

    def test_calls_tmdb_client_method(self, mock_client):
        mock_client.return_value = self.mock_response
        self.client.get("/movies/search", data={"query": "terminator", "page": 4})
        self.assertTrue(mock_client.called)

    def test_calls_tmdb_client_with_proper_page(self, mock_client):
        mock_client.return_value = self.mock_response
        self.client.get("/movies/search", data={"query": "terminator", "page": 4})
        mock_client.assert_called_with("terminator", 4)