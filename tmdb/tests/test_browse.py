from django.test import TestCase

from tmdb.browse import PopularBrowseMode
from tmdb.util import tmdb_request

import unittest


class PopularBrowseModeTest(TestCase):

    @unittest.skip
    def test_total_pages(self):
        tmdb_response = tmdb_request("GET", "movie/popular", {"page": 1})
        mpb = PopularBrowseMode(start_page = 1)
        self.assertEqual(tmdb_response["total_pages"], mpb.total_pages)

    def test_movies_has_next_is_false_for_last_page(self):
        tmdb_response = tmdb_request("GET", "movie/popular", {"page": 1})
        total_pages = tmdb_response["total_pages"]

        mpb = PopularBrowseMode(start_page = total_pages)
        self.assertTrue(mpb.has_next())
        mpb.next()
        self.assertFalse(mpb.has_next())

    def test_has_prev_is_false_for_first_page(self):
        mpb = PopularBrowseMode(start_page = 1)
        self.assertFalse(mpb.has_prev())

    @unittest.skip
    def test_movies_on_1st_page(self):
        tmdb_response = tmdb_request("GET", "movie/popular", {"page": 1})
        tmdb_movies = [ movie["title"] for movie in tmdb_response.get("results") ]

        mpb = PopularBrowseMode(start_page = 1)
        mpb_movies = mpb.next()

        self.assertTrue(all(movie["title"] in tmdb_movies for movie in mpb_movies))    

    @unittest.skip
    def test_movies_on_2nd_5st_page(self):
        tmdb_response = tmdb_request("GET", "movie/popular", {"page": 2})
        tmdb_movies = [ movie["title"] for movie in tmdb_response.get("results") ]

        mpb = PopularBrowseMode(start_page = 5)
        mpb_movies = mpb.next()

        self.assertFalse(all(movie["title"] in tmdb_movies for movie in mpb_movies))   