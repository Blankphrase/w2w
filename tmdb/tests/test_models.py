from django.test import TestCase

from tmdb.util import tmdb_request
from tmdb.models import MoviePopularQuery, Movie

import unittest
import datetime


class TMDBModelsTest(TestCase):

    def test_create_movie_and_save_it(self):
        movie = Movie(title = "Hej Ho", id = 1)
        movie.save()
        self.assertEqual(Movie.objects.count(), 1)

    def test_add_movie_to_movie_popular_query(self):
        movie1 = Movie.objects.create(title = "Hej Ho", id = 1)
        mpq = MoviePopularQuery.objects.create(
            timestamp = datetime.datetime.utcnow(), page = 1)
        mpq.movies.add(movie1)
        mpq.save()
        movie2 = Movie.objects.first()
        self.assertIn(movie2, MoviePopularQuery.objects.first().movies.all())