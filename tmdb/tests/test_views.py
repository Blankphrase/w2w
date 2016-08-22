from django.test import TestCase

from tmdb.util import tmdb_request

import json
import unittest


class TMDB_API_Test(TestCase):

    @unittest.skip
    def test_get_the_most_popular_movies(self):
        response = self.client.get("/tmdb/movie/popular", 
            data = {"force": True}
        )
        self.assertEqual(response.status_code, 200)

        movies_test = json.loads(response.content.decode()).get("results")
        movies_ref = tmdb_request("GET", "movie/popular").get("results")
        movies_ref_titles = [ movie["title"] for movie in movies_ref ]

        for movie in movies_test:
            self.assertIn(movie["title"], movies_ref_titles)

    @unittest.skip
    def test_get_the_most_popular_movies_from_10th_page(self):
        response = self.client.get("/tmdb/movie/popular", 
            data = {"force": True, "page": 10}
        )
        self.assertEqual(response.status_code, 200)

        movies_test = json.loads(response.content.decode()).get("results")
        movies_ref = tmdb_request("GET", "movie/popular", {"page": 10}).get("results")
        movies_ref_titles = [ movie["title"] for movie in movies_ref ]

        for movie in movies_test:
            self.assertIn(movie["title"], movies_ref_titles)

    def test_check_for_source_in_response(self):
        response = self.client.get("/tmdb/movie/popular", 
            data = {"page": 2}
        )
        response_json = json.loads(response.content.decode())
        self.assertIn("source", response_json)
               
    def test_save_the_most_popular_movies_query(self):
        response = self.client.get("/tmdb/movie/popular", 
            data = {"page": 2}
        )

        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json["source"], "tmdb")

        response = self.client.get("/tmdb/movie/popular", 
            data = {"page": 2}
        )
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json["source"], "w2w")