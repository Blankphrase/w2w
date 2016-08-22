from django.test import TestCase

from tmdb.util import tmdb_request
from tmdb.models import MoviePopularQuery

import unittest


class TMDBModelsTest(TestCase):

    @unittest.skip
    def test_tmdb_request_movie_fight_club(self):
        response = tmdb_request(
            method = "GET",
            path = "movie/550",
            params = None
        )
        self.assertEqual(response["title"], "Fight Club")

    @unittest.skip
    def test_save_movie_to_database(self):
        self.fail("Finish this test")

    @unittest.skip
    def test_save_twice_the_same_movie(self):
        self.fail("Finish this test")

    @unittest.skip
    def test_load_movie_from_database(self):
        self.fail("Finish this test")

    @unittest.skip
    def test_save_movie_popular_query(self):
        mpq1 = MoviePopularQuery.objects.create(page = 1)
        mpq2 = MoviePopularQuery.objects.filter(page = 1)
        self.assertEqual(mpq1, mpq2)