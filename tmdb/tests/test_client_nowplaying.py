from django.test import TestCase
from django.forms import model_to_dict

from tmdb.client import Client
from tmdb.models import (
    Movie, MoviePopularQuery, NowPlayingQuery,
    MIN_UPDATE_LEVEL, MAX_UPDATE_LEVEL, POPULAR_UPDATE_LEVEL
)
from tmdb.util import tmdb_request

import json
import unittest
from unittest.mock import patch


class ClientNowPlayingTest(TestCase):

    def setUp(self):
        self.tmdb_client = Client()

    @patch("tmdb.client.NowPlayingQuery.objects.get")
    def test_checks_for_presence_of_the_page_in_db(self, mock_get):
        self.tmdb_client.get_nowplaying_movies(page = 1)
        mock_get.assert_called_with(page = 1)


    @patch("tmdb.client.tmdb_request")
    def test_for_not_propagation_error_if_page_not_exist(self, mock_tmdb):
        try:
            self.tmdb_client.get_nowplaying_movies(page = 1)
        except NowPlayingQuery.DoesNotExist:
            self.fail("get_nowplaying_movies raised DoesNotExist unexpectedly!")


    @patch("tmdb.client.tmdb_request")
    def test_calls_tmdb_request(self, mock_tmdb):
        self.tmdb_client.get_nowplaying_movies(page = 1)
        self.assertTrue(mock_tmdb.called)


    @patch("tmdb.client.NowPlayingQuery.objects.get")
    @patch("tmdb.client.tmdb_request")
    def test_does_not_call_tmdb_request_when_page_exist(self, mock_tmdb, mock_get):
        npq = NowPlayingQuery()
        mock_get.return_value = npq
        self.tmdb_client.get_nowplaying_movies(page = 1)
        self.assertFalse(mock_tmdb.called)


    @patch("tmdb.client.tmdb_request")
    def test_for_saving_query_in_db(self, mock_tmdb):
        self.tmdb_client.get_nowplaying_movies(page = 1)
        self.assertEqual(NowPlayingQuery.objects.count(), 1)

