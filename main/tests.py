from django.test import TestCase
from django.utils.html import escape
from django.http.request import HttpRequest
from django.contrib.auth.models import User

from tmdb.util import tmdb_request
from main.views import home_page

import unittest
from lxml import etree


class HomePageTest(TestCase):

    def test_show_homepage_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_display_list_containing_20_movies(self):
        response = self.client.get("/")
        self.assertContains(response, '<ul id="movies-list">')
        self.assertEqual(
            response.content.decode().count('<li class="movie-item">'), 
            20
        )
    
    def test_show_nonempty_movies_titles(self):
        response = self.client.get("/")
        html = etree.HTML(response.content.decode())
        spans = html.xpath("//span[@class='movie-item-title']")
        for span in spans:
            self.assertNotEqual(span.text, None)
            self.assertNotEqual(span.text, "")

    def test_use_correct_movie_id_for_checkbox(self):
        response = self.client.get("/")
        response = self.client.get("/")
        html = etree.HTML(response.content.decode())
        values = html.xpath("//input[@class='movie-item-checkbox']/@value")
        self.assertFalse(any(value == "" for value in values))

    def test_display_the_most_popular_movies_on_homepage(self):
        movies = tmdb_request("GET", "movie/popular").get("results")
        self.assertIsNotNone(movies)
        response = self.client.get("/")
        for movie in movies:
            self.assertIn(escape(movie["title"]), response.content.decode())