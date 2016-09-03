from django.test import TestCase
from django.forms import model_to_dict

from tmdb.client import Client
from tmdb.models import Movie, MoviePopularQuery
from tmdb.util import tmdb_request

import json
import unittest
from unittest.mock import patch


class ClientPopularTest(TestCase):

    def setUp(self):
        self.tmdb_client = Client()


    @patch("tmdb.client.tmdb_request")
    def test_call_tmdb_request_with_the_proper_arguments(self, tmdb_request_mock):
        tmdb_request_mock.return_value = {
            "results": [ ],
            "total_results": 0, 
            "page": 2,
            "total_pages": 1
        }
        self.tmdb_client.get_popular_movies(page = 101)
        tmdb_request_mock.assert_called_once_with(method="GET", 
            path="movie/popular", params={"page": 101})
    

    @patch("requests.request")
    def test_get_the_most_popular_movies(self, request_mock):
        movies_ref = [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ]
        request_mock.return_value.json.return_value = {
            "results": movies_ref,
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }
        pq = self.tmdb_client.get_popular_movies(page = 1)     
        movies = [ {"title": movie["title"], "id": movie["id"] } for movie in pq["movies"] ]
        self.assertEqual(movies, movies_ref)


    @patch("requests.request")
    def test_save_the_most_popular_movies_in_database(self, tmdb_mock):
        tmdb_mock.return_value.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }
        self.tmdb_client.get_popular_movies()
        self.assertTrue(Movie.objects.filter(id=9).exists())
        self.assertTrue(Movie.objects.filter(id=41).exists())


    @patch("requests.request")
    def test_save_the_most_popular_movies_query(self, request_mock):
        request_mock.return_value.json.return_value = {
            "results": [ ],
            "total_results": 0, 
            "page": 1,
            "total_pages": 1
        }
        self.tmdb_client.get_popular_movies(page = 3)
        self.assertTrue(MoviePopularQuery.objects.filter(page = 3).exists())


    @patch("requests.request")
    def test_movies_related_to_popularmoviequery(self, request_mock):
        request_mock.return_value.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }
        self.tmdb_client.get_popular_movies(page = 1)
        movies = MoviePopularQuery.objects.first().movies.all()
        titles = [ movie.title for movie in movies]
        self.assertIn("0940", titles)
        self.assertIn("RGui", titles)


    @patch("requests.request")
    def test_save_only_once_the_same_popular_movies_query(self, request_mock):
        request_mock.return_value.json.return_value = {
            "results": [ ],
            "total_results": 0, 
            "page": 2,
            "total_pages": 1
        }
        self.tmdb_client.get_popular_movies(page = 2)
        self.tmdb_client.get_popular_movies(page = 2)
        self.assertEqual(MoviePopularQuery.objects.count(), 1)


    @patch("tmdb.client.tmdb_request")
    def test_call_only_once_tmdb_request_from_the_same_query(self, tmdb_mock):
        tmdb_mock.return_value = {
            "results": [ ],
            "total_results": 0, 
            "page": 2,
            "total_pages": 1
        }
        self.tmdb_client.get_popular_movies(page = 2)
        self.tmdb_client.get_popular_movies(page = 2)
        self.assertEqual(tmdb_mock.call_count, 1)


    @patch("requests.request")
    def test_save_movies_from_popular_movie_query(self, request_mock):
        request_mock.return_value.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }
        self.tmdb_client.get_popular_movies(page = 1)
        self.assertEqual(Movie.objects.count(), 2)  

    
    @patch.object(Client, "_save_movie_in_database")
    @patch("requests.request")
    def test_do_not_saved_already_stored_movies(self, request_mock, save_mock):
        request_mock.return_value.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }

        Movie.objects.create(title="0940",id=9)
        Movie.objects.create(title="RGui",id=41)
        self.tmdb_client.get_popular_movies(page = 1)

        self.assertEqual(save_mock.call_count, 0)


    @patch("requests.request")
    def test_do_not_update_popular_movies_query_without_force(self, request_mock):
        request_mock.return_value.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }       
        self.tmdb_client.get_popular_movies(page = 1)
        request_mock.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41},
                {"title": "1038", "id": 10} ],
            "total_results": 3, 
            "page": 1,
            "total_pages": 1
        }           
        mpq = self.tmdb_client.get_popular_movies(page = 1)
        self.assertEqual(mpq["total_results"], 2)


    @patch("requests.request")
    def test_force_to_update_popular_movies_query(self, request_mock):
        request_mock.return_value.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }       
        self.tmdb_client.get_popular_movies(page = 1)
        request_mock.return_value.json.return_value = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41},
                {"title": "1038", "id":10} ],
            "total_results": 3, 
            "page": 1,
            "total_pages": 1
        }           
        mpq = self.tmdb_client.get_popular_movies(page = 1, update_data = True)
        self.assertEqual(mpq["total_results"], 3)


    @patch("requests.request")
    def test_empty_popular_movie_query(self, request_mock):
        request_mock.return_value.json.return_value = {
            "results": [],
            "total_results": 0, 
            "page": 1,
            "total_pages": 1
        }
        mpq = self.tmdb_client.get_popular_movies(page = 1)
        self.assertEqual(len(mpq["movies"]), 0)
        self.assertEqual(Movie.objects.count(), 0)