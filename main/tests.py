from django.test import TestCase

import unittest


class HomePageTest(TestCase):

    def test_show_homepage_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_display_list_containing_10_movies(self):
        response = self.client.get("/")
        self.assertContains(response, '<ul id="movies-list">')
        self.assertEqual(
            response.content.decode().count('<li class="movie-item">'), 
            10
        )

    @unittest.skip
    def test_display_the_most_popular_movies(self):
        movies = self.client.post("/tmdb/movie/popular",
            data = {"page": 1})
        response = self.client.get("/")
        # Check whether response contains all title from movies
