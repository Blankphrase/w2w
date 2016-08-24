from selenium import webdriver

import unittest


class AnonymousUserRecoTest(unittest.TestCase):
    '''
    Minimum viable: User selects his/her favourite movies from the given list.
    He/She uses checkboxes located by the movies' title. Selected movies
    appears in preference lists where user can also adjust his/her
    preferecnes. After that user click button 'Ask for reco.' and the systems
    makes recommendation.
    '''

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_make_standalone_reco(self):
        # Kate has heard about a cool new web application which recommends
        # movies worth to watch. She goes check out how it works. 
        self.browser.get("http://localhost:8000")

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
            self.assertIn(kate_movies[i].text, 
                movies[i].find_element_by_class_name("movie-item-title").text
            )

        # Suddenly Kate notices in the area of initial movies list two buttons
        # with 'Prev' and 'Next' labels. She clicks next button and new list of 
        # movies appears.
        self.browser.find_element_by_id("movies-list-next")

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
        self.browser.find_element_by_id("movies-list-prev")

        # Movies' list returns to previous one.
        movies = self.browser.find_elements_by_css_selector(".movie-item")
        movies_titles_prev = [ movie.find_element_by_class_name("movie-item-title").text\
            for movie in movies ]
        self.assertTrue(all(movie_title in movies_titles\
            for movie_title in movies_titles_prev))

        # She notices that the movies she has chosen are checked.
        self.fail("Finish the test")

        # Kate decides to uncheck one movie.

        # The movie disappears from her preferences list, but there are still
        # five other movies.

        # Kate presses the button "Ask for recommendation" and waits for response. 
        # System presents list of recommended movies. 
        self.browser.find_element_by_id("ask-for-reco").click()


if __name__ == "__main__":
    unittest.main(warnings = "ignore")
