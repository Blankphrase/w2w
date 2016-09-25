from . import base

from django.contrib.auth import get_user_model


User = get_user_model()


class StandaloneRecoTest(base.FunctionalTest):
    '''
    General recommendation is made on the base of user's favourite
    movies. User has to be autenciated and needs to have some
    favourite movies chosen in the past.
    '''

    def select_favourite_movies(self, movies_pos):
        self.wait_for_movies_list_update()
        movies = self.browser.find_elements_by_css_selector(".movie-item")
        for pos in movies_pos:
            movies[pos].find_element_by_tag_name("input").click()


    def test_make_standalone_recommendation_with_default_ratings(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')
        
        # She goes to the home page and starts a standalone recommendation
        # procedure by clicing 'Standalone Recommendation' button.
        self.browser.get(self.server_url)
        self.wait_for_element_with_id("standalone-reco-btn")
        self.browser.find_element_by_id("standalone-reco-btn").click()

        # Edith selects her favourite movies from first page
        self.select_favourite_movies(movies_pos = [1, 3, 6, 9])

        # Selected movies appears in her preferences list where
        # she can additonaly adjust her preferences

        # The system automatically update her preferences list where
        # she can additionaly adjusts her past preferences.
        edith_pref = self.browser.find_element_by_id("pref-list")
        self.wait_for(lambda *args: self.assertEqual(
            len(edith_pref.find_elements_by_tag_name("li")), 4
        ))

        # Edith decideds not to modify her preferences. She just clicks
        # 'Make Recommendation' button.
        self.browser.find_element_by_id("make-reco-btn").click()

        # The system show communicate "Recommendation in progress ..."
        # and Edith waits for her movies.
        self.wait_for_element_with_id("reco-status")
        reco_status = self.browser.find_element_by_id("reco-status")
        self.assertIn("Recommendation in progres ...", reco_status.text)

        # After a while the communicate disappears
        self.wait_for(lambda *args:
            self.assertNotIn("Recommendation in progres ...", reco_status.text),
            timeout = 30
        )

        # List of recommended movies appears. 
        edith_reco = self.browser.find_element_by_id("reco-list")
        reco_movies = edith_reco.find_elements_by_tag_name("li")
        self.assertGreater(len(reco_movies), 0)