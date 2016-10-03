from tmdb.client import Client
from tmdb.models import Movie, MoviePopularQuery

from django.test import TestCase

import json
from unittest.mock import patch


@patch("tmdb.client.tmdb_request")
class PopularMoviesTest(TestCase):

    def setUp(self):
        movie_1 = Movie.objects.create(title = "Excel", id = 1)
        movie_2 = Movie.objects.create(title = "Word", id = 2)
        movie_3 = Movie.objects.create(title = "Access", id = 3)

        self.mpq1 = MoviePopularQuery.objects.create(page = 1, 
            total_pages = 3, total_results = 3)
        self.mpq1.movies.add(movie_1)
        self.mpq2 = MoviePopularQuery.objects.create(page = 2, 
            total_pages = 3, total_results = 3)
        self.mpq2.movies.add(movie_2)
        self.mpq3 = MoviePopularQuery.objects.create(page = 3, 
            total_pages = 3, total_results = 3)
        self.mpq3.movies.add(movie_3)
        

    def test_movies_popular_returns_first_page(self, tmdb_mock):
        tmdb_mock.return_value = {}
        response = self.client.get("/movies/popular")  
        movies = json.loads(response.content.decode())["movies"]
        self.assertEqual(movies[0]["title"], self.mpq1.movies.all()[0].title)


    def test_movies_popular_next_page(self, tmdb_mock):
        tmdb_mock.return_value = {} 
        self.client.post("/movies/popular")
        response = self.client.post("/movies/next")
        movies = json.loads(response.content.decode())["movies"]
        self.assertEqual(movies[0]["title"], self.mpq2.movies.all()[0].title)


    def test_movies_popular_next_page_twice(self, tmdb_mock):
        tmdb_mock.return_value = {}
        self.client.post("/movies/popular")
        self.client.post("/movies/next")
        response = self.client.post("/movies/next")
        movies = json.loads(response.content.decode())["movies"]
        self.assertEqual(movies[0]["title"], self.mpq3.movies.all()[0].title)


    def test_movies_popular_no_more_next(self, tmdb_mock):
        tmdb_mock.return_value = {
            "results": [],
            "total_pages": 3,
            "total_results": 3,
            "page": 4
        }
        self.client.post("/movies/popular")
        self.client.post("/movies/next")
        self.client.post("/movies/next")
        response = json.loads(self.client.post("/movies/next").content.decode())
        self.assertEqual(response["page"], 4)
        self.assertEqual(response["movies"], [])


    def test_movies_popular_no_more_prev(self, tmdb_mock):
        tmdb_mock.return_value = {}
        self.client.post("/movies/popular")
        response = json.loads(self.client.post("/movies/prev").content.decode())
        self.assertEqual(response["page"], 0)
        self.assertEqual(response["movies"], [])
    

    def test_movies_popular_next_and_prev_combination(self, tmdb_mock):
        tmdb_mock.return_value = {}
        resp_init = self.client.post("/movies/popular")
        movies_init = json.loads(resp_init.content.decode())["movies"]
        self.client.post("/movies/next")
        resp_prev = self.client.post("/movies/prev")
        movies_prev = json.loads(resp_prev.content.decode())["movies"]
        self.assertEqual(movies_prev, movies_init)


    def test_movies_popular_select_page(self, tmdb_mock):
        tmdb_mock.return_value = {}
        self.client.post("/movies/popular")
        response = self.client.post("/movies/page/3")
        movies = json.loads(response.content.decode())["movies"]
        self.assertEqual(movies[0]["title"], self.mpq3.movies.all()[0].title)
    
    
    def test_movies_popular_page_out_of_range(self, tmdb_mock):
        tmdb_mock.return_value = {
            "results": [],
            "total_pages": 3,
            "total_results": 3,
            "page": 999
        }
        self.client.post("/movies/popular")
        response = json.loads(self.client.post("/movies/page/999").content.decode())
        self.assertEqual(response["page"], 999)
