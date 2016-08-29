from django.test import TestCase
from django.test.client import Client
from django.utils.html import escape
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.urls import reverse

from tmdb.util import tmdb_request
from main.views import home_page
from tmdb.models import Movie
import main.browse as browse

import json
import unittest
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

    # @unittest.skip
    def test_display_the_most_popular_movies_on_homepage(self):
        movies = tmdb_request("GET", "movie/popular").get("results")
        self.assertIsNotNone(movies)
        response = self.client.get("/")
        for movie in movies:
            self.assertIn(escape(movie["title"]), response.content.decode())


class BrowseMoviesTest(TestCase):


    def test_reverse_movies_browse_with_page(self):
        movies_url = reverse("movies_browse_page", kwargs={"page": 3})
        self.assertEqual(movies_url, "/movies/browse/page/3")

    # @unittest.skip
    def test_load_movies_using_ajax_request(self):
        movies_tmdb = tmdb_request("GET", "movie/popular", 
            {"page": 3}).get("results")
        movies_titles = [ movie["title"] for movie in movies_tmdb ]

        self.assertEqual(Movie.objects.all().count(), 0)
        movies = json.loads(self.client.post(
            reverse("movies_browse_page", kwargs={"page": 3})
        ).content.decode())

        self.assertTrue(all(movie["title"] in movies_titles for movie in movies))

    # @unittest.skip
    def test_load_autoamtically_next_movies_using_ajax(self):
        movies_tmdb = tmdb_request("GET", "movie/popular",
            {"page": 2}).get("results")
        movies_titles = [ movie["title"] for movie in movies_tmdb ]

        self.client.get("/") # load page 1
        response = self.client.post("/movies/browse/next")
        movies = json.loads(response.content.decode()) # load page 2
        self.assertTrue(all(movie["title"] in movies_titles for movie in movies))


    # def test_keep_user_movie_choices_within_server_session(self):
    #     movies = browse.get_movies({"mode": "popular", "page": 1})

    #     self.client.get("/")
    #     response = self.client.post("/movies/browse/check",
    #         { "tmdb_id": movies[0]["tmdb_id"] }) 
    #     self.assertEqual(response.status_code, 200)    
    #     self.client.post(reverse("browse_check"), 
    #         {"tmdb_id": movies[1]["tmdb_id"]})

    #     session = self.client.session
    #     self.assertIn(movies[0]["tmdb_id"], session["browse_selected"])
    #     self.assertIn(movies[1]["tmdb_id"], session["browse_selected"])