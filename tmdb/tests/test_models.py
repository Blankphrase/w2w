from django.test import TestCase

from tmdb.util import tmdb_request
from tmdb.models import (
    MoviePopularQuery, Movie, NowPlayingQuery,
    POPULAR_UPDATE_LEVEL
)

import unittest
from unittest.mock import patch
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


class MovieTest(TestCase):

    @patch("tmdb.models.Movie.objects.get")
    def test_querying_db_for_wanted_movie(self, mock_get):
        movie = Movie.get(id = 1)
        self.assertTrue(mock_get.called)


    def test_get_returns_correct_movie_object(self):
        Movie.objects.create(id = 1)
        movie = Movie.get(id = 1)
        self.assertEqual(movie.id, 1)       


    @patch("tmdb.models.tmdb_request")
    def test_calls_tmdb_request_if_movie_does_not_exist(self, mock_tmdb):
        mock_tmdb.return_value = {"id": 1, "title": "JAGO 2000"}
        movie = Movie.get(id = 1)
        mock_tmdb.assert_called_with(method = "GET", path = "movie/1")


    @patch("tmdb.models.tmdb_request")
    def test_raise_error_when_offline(self, mock_tmdb):
        mock_tmdb.return_value = {"id": 1, "title": "JAGO 2000"}
        with self.assertRaises(Movie.DoesNotExist):
            movie = Movie.get(id = 1, offline = True)


    @patch("tmdb.models.tmdb_request")
    def test_saves_new_movie_in_db(self, mock_tmdb):
        mock_tmdb.return_value = {"id": 1, "title": "JAGO 2000"}
        movie = Movie.get(id = 1)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(movie.id, 1)


    @patch("tmdb.models.tmdb_request")
    def test_raises_error_movie_does_not_exist_in_tmdb(self, mock_tmdb):
        mock_tmdb.return_value = {"status_code": 34}
        with self.assertRaises(Movie.DoesNotExist):
            movie = Movie.get(id = 1)


    @patch("tmdb.models.tmdb_request")
    def test_calls_tmdb_request_if_two_low_update_level(self, mock_tmdb):
        Movie.objects.create(id = 1, title = "JAGO 2000", update_level = 0)
        mock_tmdb.return_value = {"id": 1, "title": "JAGO 2000"}
        movie = Movie.get(id = 1, min_update_level = POPULAR_UPDATE_LEVEL)
        mock_tmdb.assert_called_with(method = "GET", path = "movie/1")


    @patch("tmdb.models.tmdb_request")   
    def test_calls_tmdb_request_when_force_update(self, mock_tmdb):
        Movie.objects.create(id = 1, title = "JAGO 2000", update_level = 100)
        mock_tmdb.return_value = {"id": 1, "title": "JAGO 2000"}
        movie = Movie.get(id = 1, force_update = True)
        mock_tmdb.assert_called_with(method = "GET", path = "movie/1")



@patch("tmdb.models.tmdb_request")
class NowPlayingQueryTest(TestCase):

    def setUp(self):
        self.tmdb_return = {
            "results": [ {"title": "0940", "id": 9}, {"title": "RGui", "id": 41} ],
            "total_results": 2, 
            "page": 1,
            "total_pages": 1
        }

    def test_get_returns_npq_object(self, mock_tmdb):
        npq = NowPlayingQuery.get(page = 1)
        self.assertIsInstance(npq, NowPlayingQuery)

    @patch ("tmdb.models.NowPlayingQuery.objects.get")
    def test_checks_for_presence_of_the_page_in_db(self, mock_get, mock_tmdb):
        npq = NowPlayingQuery.get(page = 1)
        self.assertTrue(mock_get.called)

    def test_for_not_propagation_error_if_page_not_exist(self, mock_tmdb):
        try:
            npq = NowPlayingQuery.get(page = 1)
        except NowPlayingQuery.DoesNotExist:
            self.fail("get raised DoesNotExist unexpectedly!")

    def test_returns_proper_npq_if_exists(self, mock_tmdb):
        npq_base = NowPlayingQuery.objects.create(page = 1)
        npq = NowPlayingQuery.get(page = 1)
        self.assertEqual(npq, npq_base)

    def test_saves_new_npq_in_db(self, mock_tmdb):
        npq = NowPlayingQuery.get(page = 1)
        self.assertEqual(NowPlayingQuery.objects.count(), 1)

    def test_calls_tmdb_request(self, mock_tmdb):
        NowPlayingQuery.get(page = 1)
        mock_tmdb.assert_called_with(
            method = "GET", 
            path = "movie/nowplaying", 
            params = {"page": 1}
        )

    def test_saves_new_movies_in_db(self, mock_tmdb):
        mock_tmdb.return_value.json.return_value = self.tmdb_return
        NowPlayingQuery.get(page = 1)
        mock_tmdb.assert_called_with(
            method = "GET", 
            path = "movie/nowplaying", 
            params = {"page": 1}
        )
        self.assertTrue(Movie.objects.count(), 2)