from . import base

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import time


class GeneralRecoTest(base.FunctionalTest):
    '''
    General recommendation is made on the base of user's favourite
    movies. User has to be autenciated and needs to have some
    favourite movies chosen in the past.
    '''

    def create_pre_authenitcated_session(self, email):
        pass

    def select_favourite_movies(self):
        pass

    def test_make_general_recommedation_wo_pref_adjustments(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')

        # Edith has already chosen her favourite movies in the past
        self.select_favourite_movies()

        # She goes to the home page and starts a general recommendation
        # procedure by clicing 'General Recommendation' button.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id("general-reco-btn").click()

        # The system automatically populates her preferences list where
        # she can additionaly adjusts her past preferences.
        edith_pref = self.browser.find_element_by_id("pref-list")
        edith_movies = kate_pref.find_elements_by_tag_name("li")
        self.assertEqual(len(kate_movies), 10)

        # Edith decideds not to modify her preferences. She just clicks
        # 'Make Recommendation' button.
        self.browser.find_element_by_id("make-reco-btn").click()

        # The system show communicate "Recommendation in progress ..."
        # and Edith waits for her movies.
        reco_status = self.browser.find_element_by_id("reco-status").text
        self.assertIn("Recommendation in progres ...", reco_status)

        self.wait_for_element_to_hide(reco_status)

        # After a while the communicate disapears and the list of
        # recommended movies appears. 
        edith_reco = self.browser.find_element_by_id("reco-list")
        reco_movies = edith_reco.find_elements_by_tag_name("li")
        self.assertGreater(len(reco_movies), 0)