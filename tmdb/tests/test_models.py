from django.test import TestCase

from tmdb.util import tmdb_request

import unittest


class TMDBModelsTest(TestCase):

    def test_tmdb_request_movie_fight_club(self):
        response = tmdb_request(
            method = "GET",
            path = "movie/550",
            params = None
        )
        self.assertEqual(response["title"], "Fight Club")

    def test_save_movie_to_database(self):
        self.fail("Finish this test")

    def test_save_twice_the_same_movie(self):
        self.fail("Finish this test")

    def test_load_movie_from_database(self):
        self.fail("Finish this test")

    