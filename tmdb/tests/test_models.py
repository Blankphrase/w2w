import unittest
from unittest.mock import patch
import datetime

from django.test import TestCase
from requests.exceptions import RequestException

from tmdb.util import tmdb_request
from tmdb.models import (
    MoviePopularQuery, Movie, NowPlayingQuery, Genre
)


class GenreTest(TestCase):

    def test_contains_id_title_and_movies_fields(self):
        genre = Genre.objects.create(id=18, name="Drama")
        self.assertIsNotNone(genre.id)
        self.assertIsNotNone(genre.name)
        self.assertIsNotNone(genre.movies)

    def test_cannot_create_two_genres_with_the_same_name(self):
        genre1 = Genre.objects.create(id=18, name="Drama")
        with self.assertRaises(Exception):
            genre2 = Genre.objects.create(id=19, name="Drama")

    def test_add_movie_adds_movie_to_movies(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        movie_other = Movie.objects.create(id=2, title="Titanic2")
        genre.add_movie(id=1)
        self.assertEqual(genre.movies.count(), 1)
        self.assertEqual(genre.movies.first().id, 1)

    def test_add_movie_raises_error_when_id_and_movie(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        with self.assertRaises(RuntimeError):
            genre.add_movie(id = 1, movie = movie)

    def test_add_movie_raises_error_when_no_id_and_movie(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        with self.assertRaises(RuntimeError):
            genre.add_movie()

    def test_cannot_add_twice_the_same_movie_to_genre(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        movie_other = Movie.objects.create(id=2, title="Titanic2")
        genre.add_movie(id=1)
        genre.add_movie(id=1)
        self.assertEqual(genre.movies.count(), 1)
        self.assertEqual(genre.movies.first().id, 1)
       
    def test_cannot_add_not_existing_movie(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        with self.assertRaises(Movie.DoesNotExist):
            genre.add_movie(id=2)

    def test_remove_movie_removes_only_relation(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        genre.add_movie(id=1)
        genre.remove_movie(id=1)
        self.assertEqual(genre.movies.count(), 0)
        self.assertEqual(Movie.objects.count(), 1)

    def test_remove_movie_by_obj(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        genre.add_movie(id=1)
        genre.remove_movie(movie=movie)     
        self.assertEqual(genre.movies.count(), 0)

    def test_remove_movie_raises_error_when_id_and_movie(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        genre.add_movie(movie=movie)
        with self.assertRaises(RuntimeError):
            genre.remove_movie(id = 1, movie = movie)

    def test_remove_movie_raises_error_when_no_id_and_movie(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        genre.add_movie(movie=movie)
        with self.assertRaises(RuntimeError):
            genre.remove_movie()


    @patch("tmdb.models.tmdb_request")
    def test_update_genres_calls_tmdb_request(self, mock_request):        
        Genre.update_genres()
        self.assertTrue(mock_request.called)

    @patch("tmdb.models.tmdb_request")
    def test_updates_genres_in_database(self, mock_request):
        mock_request.return_value = {
            "genres": [
                {"id": 28, "name": "Action"},
                {"id": 12, "name": "Adventure"}
            ]
        }
        updated = Genre.update_genres()
        self.assertEqual(Genre.objects.count(), 2)
        self.assertEqual(
            set([28, 12]), 
            set(Genre.objects.values_list("id", flat=True).all())
        )
        self.assertEqual(updated, 2)

    @patch("tmdb.models.tmdb_request")
    def test_updates_genres_returns_zero_when_exception(self, mock_request):
        mock_request.side_effect = RequestException()
        updated = Genre.update_genres()
        self.assertEqual(updated, 0)


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
        movie = Movie.get(id = 1, 
            min_update_level = MoviePopularQuery.update_level)
        mock_tmdb.assert_called_with(method = "GET", path = "movie/1")

    @patch("tmdb.models.tmdb_request")   
    def test_calls_tmdb_request_when_force_update(self, mock_tmdb):
        Movie.objects.create(id = 1, title = "JAGO 2000", update_level = 100)
        mock_tmdb.return_value = {"id": 1, "title": "JAGO 2000"}
        movie = Movie.get(id = 1, force_update = True)
        mock_tmdb.assert_called_with(method = "GET", path = "movie/1")

    @patch("tmdb.models.tmdb_request")
    def test_propagates_request_exception(self, mock_tmdb):
        mock_tmdb.side_effect = RequestException()
        with self.assertRaises(RequestException):
            movie = Movie.get(id = 1, force_update = True)

    def test_adds_movie_to_genre_by_genre_add_movie(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        genre.add_movie(movie=movie)
        self.assertEqual(movie.genres.count(), 1)
        self.assertEqual(movie.genres.first().name, "Drama")

    def test_adds_movie_to_genre_by_add_to_genre(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        movie.add_to_genre(genre=genre)
        self.assertEqual(movie.genres.count(), 1)
        self.assertEqual(movie.genres.first().name, "Drama")        

    def test_adds_movie_to_genre_by_add_to_genre_with_id(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        movie.add_to_genre(id = 1)
        self.assertEqual(movie.genres.count(), 1)
        self.assertEqual(movie.genres.first().name, "Drama")        

    def test_removes_movie_from_genre(self):
        genre = Genre.objects.create(id=1, name="Drama")
        movie = Movie.objects.create(id=1, title="Titanic")
        movie.add_to_genre(genre=genre)
        movie.remove_from_genre(id=1)
        self.assertEqual(movie.genres.count(), 0)



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
        mock_tmdb.return_value = self.tmdb_return
        npq = NowPlayingQuery.get(page = 1)
        self.assertIsInstance(npq, NowPlayingQuery)

    @patch ("tmdb.models.NowPlayingQuery.objects.get")
    def test_checks_for_presence_of_the_page_in_db(self, mock_get, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return
        npq = NowPlayingQuery.get(page = 1)
        self.assertTrue(mock_get.called)

    def test_for_not_propagation_error_if_page_not_exist(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return
        try:
            npq = NowPlayingQuery.get(page = 1)
        except NowPlayingQuery.DoesNotExist:
            self.fail("get raised DoesNotExist unexpectedly!")

    def test_returns_proper_npq_if_exists(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return
        npq_base = NowPlayingQuery.objects.create(page = 1)
        npq = NowPlayingQuery.get(page = 1)
        self.assertEqual(npq, npq_base)

    def test_saves_new_npq_in_db(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return
        npq = NowPlayingQuery.get(page = 1)
        self.assertEqual(NowPlayingQuery.objects.count(), 1)

    def test_calls_tmdb_request(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return
        NowPlayingQuery.get(page = 1)
        mock_tmdb.assert_called_with(
            method = "GET", 
            path = "movie/now_playing", 
            params = {"page": 1}
        )

    def test_saves_new_movies_in_db(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return
        NowPlayingQuery.get(page = 1)
        mock_tmdb.assert_called_with(
            method = "GET", 
            path = "movie/now_playing", 
            params = {"page": 1}
        )
        self.assertTrue(Movie.objects.count(), 2)

    def test_updates_only_selected_movies(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return 
        Movie.objects.create(id = 9, title = "Nine", update_level = 0)
        Movie.objects.create(id = 41, title = "FortyOne", update_level = 100)
        npq = NowPlayingQuery.get(page = 1)
        self.assertEqual(Movie.objects.get(id = 41).title, "FortyOne")
        self.assertNotEqual(Movie.objects.get(id = 9).title, "Nine")

    def test_associates_movies_with_npq(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return        
        npq = NowPlayingQuery.get(page = 1)       
        self.assertEqual(npq.movies.count(), 2)
        self.assertEqual(
            set(npq.movies.values_list("id", flat=True)), 
            set([9, 41])
        )

    @patch("tmdb.models.Movie.save_movie_in_db")
    def test_does_not_call_save_movie_in_db_if_not_required(
        self, mock_save, mock_tmdb
    ):
        mock_tmdb.return_value = self.tmdb_return 
        Movie.objects.create(id = 9, title = "Nine", update_level = 100)
        Movie.objects.create(id = 41, title = "FortyOne", update_level = 100)   
        npq = NowPlayingQuery.get(page = 1)
        self.assertFalse(mock_save.called)

    def test_updates_npq_and_movies_when_movies_with_low_update_level(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return        
        npq = NowPlayingQuery.objects.create(page = 1)
        movie1 = Movie.objects.create(id = 9, title = "Nine", update_level = 0)
        movie2 = Movie.objects.create(id = 41, title = "FortyOne", update_level = 100)   
        npq.movies.add(movie1)

        npq = NowPlayingQuery.get(page = 1)

        self.assertTrue(Movie.objects.get(id = 9).title, "0940")
        self.assertTrue(Movie.objects.get(id = 41).title, "FortyOne")
        self.assertEqual(NowPlayingQuery.objects.first().movies.count(), 2)

    def test_updates_npq_and_movies_when_force_update(self, mock_tmdb):
        mock_tmdb.return_value = self.tmdb_return  
        npq = NowPlayingQuery.objects.create(page = 1)
        movie1 = Movie.objects.create(id = 9, title = "Nine", update_level = 100)
        npq.movies.add(movie1)

        npq = NowPlayingQuery.get(page = 1, force_update = True)

        self.assertTrue(Movie.objects.get(id = 9).title, "Nine")
        self.assertEqual(NowPlayingQuery.objects.first().movies.count(), 2)
   