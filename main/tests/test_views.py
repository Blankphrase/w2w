from django.test import TestCase
from django.test.client import Client
from django.utils.html import escape
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.urls import reverse

from tmdb.util import tmdb_request
from main.views import home_page, new_reco
from tmdb.models import Movie

import json
import unittest
from unittest.mock import Mock, patch
from lxml import etree


class HomePageTest(TestCase):

    # @unittest.skip
    def test_show_homepage_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    # @unittest.skip
    def test_show_nonempty_movies_titles(self):
        response = self.client.get("/")
        html = etree.HTML(response.content.decode())
        spans = html.xpath("//span[@class='movie-item-title']")
        for span in spans:
            self.assertNotEqual(span.text, None)
            self.assertNotEqual(span.text, "")

    # @unittest.skip
    def test_use_correct_movie_id_for_checkbox(self):
        response = self.client.get("/")
        response = self.client.get("/")
        html = etree.HTML(response.content.decode())
        values = html.xpath("//input[@class='movie-item-checkbox']/@value")
        self.assertFalse(any(value == "" for value in values))

    @unittest.skip
    def test_display_the_most_popular_movies_on_homepage(self):
        movies = tmdb_request("GET", "movie/popular").get("results")
        self.assertIsNotNone(movies)
        response = self.client.get("/")
        for movie in movies:
            self.assertIn(escape(movie["title"]), response.content.decode())


# UserSource, JsonSource, FileSource


class RecoTest(unittest.TestCase):

    def setUp(self):

        self.preferences = [
            { "title": "Killer", "id": 10, "rating": 8 },
            { "title": "Spiderman", "id": 19, "rating": 6 },
            { "title": "Terminator 2", "id": 5, "rating": 10 }
        ]

        self.reco = [
            { "title": "Killer 2", "id": 11},
            { "title": "Batman Beginning", "id": 100 },
            { "title": "Terminator", "id": 50 }
        ]


    def createGeneralRequest(self, user):
        request = HttpRequest()
        request.POST["reco-type"] = "general"
        request.user = user
        return request

    def createStandaloneRequest(self, user = None):
        request = HttpRequest()
        request.POST["reco-type"] = "standalone"
        request.POST["reco-pref"] = json.dumps(self.preferences)
        request.user = user
        return request


    @patch("main.views.JsonSource")
    @patch("main.views.UserSource")
    def test_initialises_user_source_with_user_when_general(
        self, mock_user_source, mock_json_source
    ):
        request = self.createGeneralRequest(user = User())
        new_reco(request)
        mock_user_source.assert_called_once_with(user = request.user)
        self.assertFalse(mock_json_source.called)


    @patch("main.views.JsonSource")
    @patch("main.views.UserSource")
    def test_initialises_json_source_with_reco_data_when_standalone(
        self, mock_user_source, mock_json_source
    ):
        request = self.createStandaloneRequest()
        new_reco(request)
        self.assertFalse(mock_user_source.called)
        mock_json_source.assert_called_once_with(
            preferences = request.POST["reco-pref"]
        )

    @patch("main.views.UserSource")
    @patch("main.views.RecoEngine")
    def test_initialises_recoengine_with_source(
        self, mock_reco, mock_user_source
    ):
        mock = Mock()
        mock_user_source.return_value = mock
        mock_reco.return_value.make_reco.return_value = {}

        request = self.createGeneralRequest(user = User())
        new_reco(request)

        mock_reco.assert_called_once_with(source = mock)


    @patch("main.views.UserSource")
    @patch("main.views.RecoEngine")
    def test_calls_make_reco(
        self, mock_reco, mock_user_source
    ):
        mock_make_reco = Mock()
        mock_reco.return_value.make_reco = mock_make_reco
        mock_reco.return_value.make_reco.return_value = {}

        request = self.createGeneralRequest(user = User())
        new_reco(request)

        self.assertTrue(mock_make_reco.called, "call make_reco")


    @patch("main.views.UserSource")
    @patch("main.views.RecoEngine")
    @patch("main.views.JsonResponse")
    def test_returns_reco_through_json_response(
        self, mock_json, mock_engine, mock_user_source
    ):
        mock_engine.return_value.make_reco.return_value = self.reco

        request = self.createGeneralRequest(user = User())
        new_reco(request)

        mock_json.assert_called_once_with(
            {"status": "ok", "movies": self.reco}, safe = False
        )