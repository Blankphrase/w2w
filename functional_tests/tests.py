from selenium import webdriver

import unittest


class AnonymousUserRecoTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_make_standalone_reco(self):
        # Kate has heard about a cool new web application which recommends
        # movies worth to watch. She goes check out how it works. 
        self.browser.get("http://localhost:8000")

        # She notices the list of 10 different movies' titles and message 
        # informing that she can choose (by clicing) her favourite movies 
        # from given list.
        movies = self.browser.find_elements_by_css_selector(".movie-item")
        self.assertEqual(len(movies), 10)

        # Kate find three movies that she watched recently and choose them.
        # Chosen movies appear in the list titled "Movies preferences".

        # Kate compares whether appeared movies are execly thoes she
        # has selected from the list.

        self.fail("Finish the test!")


if __name__ == "__main__":
    unittest.main(warnings = "ignore")