from selenium import webdriver

import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_display_list_of_the_most_popular_movies(self):
        # Kate has heard about a cool new web application which recommends
        # movies worth to watch. She goes check out how it works. 
        self.browser.get("http://localhost:8000")

        # She notices the list of movies and message informing that
        # she can choose (by clicing) her favourite movies from given list.

        # Kate find three movies that she watched recently and choose them.
        # Chosen movies appears in the list below titled "Your preferences".

        # Kate compares whether appeared movies are execly thoes she
        # has selected from the list.

        self.fail("Finish the test!")


if __name__ == "__main__":
    unittest.main(warnings = "ignore")