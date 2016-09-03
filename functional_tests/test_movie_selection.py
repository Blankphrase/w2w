from . import base

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import time


class PopularMovieSelectionTest(base.FunctionalTest):
    '''
    Minimum viable: User selects his/her favourite movies from the given list.
    He/She uses checkboxes located by the movies' title. Selected movies
    appears in preference lists where user can also adjust his/her
    preferecnes. After that user click button 'Ask for reco.' and the systems
    makes recommendation.
    '''

    def test_movie_selection(self):
        # Kate has heard about a cool new web application which recommends
        # movies worth to watch. She goes check out how it works. 
        self.browser.get(self.server_url)

        # She notices the list of 10 different movies' titles and message 
        # informing that she can choose (with checkbox) her favourite movies 
        # from given list.
        movies = self.browser.find_elements_by_css_selector(".movie-item")

        self.assertEqual(len(movies), 20)

        # Test whether movies' titles are not empty.
        for movie in movies:
            self.assertNotEqual(
                movie.find_element_by_class_name("movie-item-title").text,
                ""
            )
        
        # Test whether movies' titles are different.
        movies_titles = [ movie.find_element_by_class_name("movie-item-title").text\
            for movie in movies ]
        self.assertEqual(len(movies_titles), len(set(movies_titles)))

        # Kate find three movies that she watched recently and choose them.
        # Chosen movies appear in the list titled "Movies preferences".
        movies[0].find_element_by_tag_name("input").click()
        movies[1].find_element_by_tag_name("input").click()
        movies[2].find_element_by_tag_name("input").click()

        # Kate compares whether appeared movies are execly those she
        # has selected from the list.
        kate_pref = self.browser.find_element_by_id("pref-list")
        kate_movies = kate_pref.find_elements_by_tag_name("li")
        self.assertEqual(len(kate_movies), 3)
        for i in range(3):
            self.assertIn(kate_movies[i].find_element_by_css_selector(".pref-item-title").text, 
                movies[i].find_element_by_class_name("movie-item-title").text
            )

        # Suddenly Kate notices in the area of initial movies list two buttons
        # with 'Prev' and 'Next' labels. She clicks next button and new list of 
        # movies appears.
        self.browser.find_element_by_id("movies-list-next").click()
        time.sleep(5)

        # New list is quite different from the previous one
        movies = self.browser.find_elements_by_css_selector(".movie-item")
        movies_titles_new = [ movie.find_element_by_class_name("movie-item-title").text\
            for movie in movies ]
        self.assertFalse(any(movie_title in movies_titles\
            for movie_title in movies_titles_new))

        # Kate finds more movies she liked on the new lists and checks them.
        movies[0].find_element_by_tag_name("input").click()
        movies[1].find_element_by_tag_name("input").click()
        movies[2].find_element_by_tag_name("input").click()        

        # Her preferences lists grows by 3 new movies
        kate_pref = self.browser.find_element_by_id("pref-list")
        kate_movies = kate_pref.find_elements_by_tag_name("li")
        self.assertEqual(len(kate_movies), 6)

        # Kate clicks left arrow below the movies' list.
        self.browser.find_element_by_id("movies-list-prev").click()

        # Movies' list returns to previous one.
        movies = self.browser.find_elements_by_css_selector(".movie-item")
        movies_titles_prev = [ movie.find_element_by_class_name("movie-item-title").text\
            for movie in movies ]
        self.assertTrue(all(movie_title in movies_titles\
            for movie_title in movies_titles_prev))

        # She notices that the movies she has chosen are checked.
        self.assertTrue(movies[0].find_element_by_tag_name("input").is_selected());
        self.assertTrue(movies[1].find_element_by_tag_name("input").is_selected());
        self.assertTrue(movies[2].find_element_by_tag_name("input").is_selected());

        # Kate decides to uncheck one movie.
        movie_unchecked = movies[0].find_element_by_tag_name("span").text;
        movies[0].find_element_by_tag_name("input").click();

        # The movie disappears from her preferences list, but there are still
        # five other movies.
        kate_pref = self.browser.find_element_by_id("pref-list")
        kate_movies = kate_pref.find_elements_by_tag_name("li")
        self.assertTrue(all(movie_unchecked not in movie.text for movie in kate_movies))
        self.assertEqual(len(kate_movies), 5)

        # Kate wants to adjust her preferences. To her luck there are ten radio 
        # buttons by every movie she chosen. 
        kate_pref = self.browser.find_element_by_id("pref-list")
        kate_movies = kate_pref.find_elements_by_tag_name("li")
        self.assertEqual(len(kate_movies[i].find_element_by_tag_name("form").\
            find_elements_by_tag_name("input")), 10)

        # Currently her preferences are set to maximum (10).
        self.assertEqual(
            len(self.browser.find_elements_by_xpath("//form[input/@value='10']")),
            5)  

        # Kate adjusts her reting for first movie to 5
        kate_movies[0].find_element_by_xpath(".//input[@value='5']").click()
        self.assertTrue(self.browser.\
            find_element_by_xpath("//input[@value='5']").is_selected()
        )

        # Kate notices also remove button near the movie title.
        kate_movies = kate_pref.find_elements_by_tag_name("li")
        self.assertTrue(all(movie.find_element_by_tag_name("button").text == "Remove"
            for movie in kate_movies));

        # Kate removes the last movie from her movies list
        kate_movies[-1].find_element_by_tag_name("button").click();

        # There are four movies left
        kate_pref = self.browser.find_element_by_id("pref-list")
        kate_movies = kate_pref.find_elements_by_tag_name("li")
        self.assertEqual(len(kate_movies), 4)


class SearchMovieSelectionTest(base.FunctionalTest):

    def test_search_movies(self):
        # Kate visits her favourite movies site.
        self.browser.get(self.server_url)
        self.wait_for_movies_list_update()

        movies = self.browser.find_elements_by_css_selector(".movie-item")
        movies_titles = [ movie.find_element_by_class_name("movie-item-title").text\
            for movie in movies ]

        # She spots new input element with placeholder 'Search for movies ...'
        search_input = self.browser.find_element_by_id("movie-search-input");
        self.assertEqual(
            search_input.get_attribute("placeholder"),
            "Search for movies ..."
        )

        # She enters 'Terminator' and presses enter
        search_input.send_keys("Terminator")
        search_input.send_keys(Keys.ENTER)

        self.wait_for_movies_list_update(retries = 5)
        
        # Previous list of movies disappears and movies related to
        # her query appears.
        movies = self.browser.find_elements_by_css_selector(".movie-item")
        movies_new_titles = [ movie.find_element_by_class_name("movie-item-title").text\
            for movie in movies ]

        self.assertFalse(
            [title for title in movies_new_titles if title in movies_titles]
        )

        # She checks first three movies as her favourite
        movies = self.browser.find_elements_by_css_selector(".movie-item")

        movies[0].find_element_by_tag_name("input").click()
        movies[1].find_element_by_tag_name("input").click()
        movies[2].find_element_by_tag_name("input").click()  

        # She decideds to search for other movies and inputs into
        # search box 'Tranlorders', and presses enter.
        search_input.send_keys("Tranlorders")
        search_input.send_keys(Keys.ENTER)

        self.wait_for_movies_list_update(retries = 5)

        # Unfortuantely, search engine was not able to find any
        # movie related to her query and she notices message
        # 'No movies found'.
        movies = self.browser.find_elements_by_css_selector(".movie-item")
        self.assertEqual(len(movies), 0)

        # She clears the input box and the list of the most popular
        # movies appears.
        self.fail("Finish the test")
        
        # She enters now correct word 'Transformers' and now the movies
        # appears.

        # She picks the first one

        # Finally there are 4 movies in her preferences list