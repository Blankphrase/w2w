from django.test import TestCase

from tmdb.util import tmdb_request

import unittest


class TMDB_API_Test(TestCase):

    @unittest.skip
    def test_movie_popular_page_1(self):
        response = self.client.post("/tmdb/movie/popular",
            data = {"page: 1"})
