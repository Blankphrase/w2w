from . import base


TEST_EMAIL = "crane@jago.com"
PASSWORD_TEST = "crane"


class StandaloneRecoTest(base.FunctionalTest):

    def test_create_account(self):
        # Crane visits his favourite site for moving recommendation
        self.browser.get(self.server_url)

        # He decides to create an account and takas adventage of all
        # functionalities available for authenitcated users. He notces
        # signup button located in upper navigation bar and clicks it.
        self.browser.find_element_by_link_text("Sign Up").click()

        # New site appears with title 'W2W - Create new account', where 
        # he has to enter his email as well as password. The password 
        # need to be confirm.
        self.wait_for(
            lambda *args: self.assertIn("W2W - Create new account", 
                self.browser.title)
        )
        
        # Crane enters his email: crane@jago.com and hit post button
        self.browser.find_element_by_id("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_tag_name("button").click()
        
        # The page informs him that he had not enter his password
        self.wait_for_element_with_class(".has-error")
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have empty password")

        # Crane enters password and its confirmation, the email has been
        # filled.
        self.assertEqual(
            self.browser.find_element_by_id("email").value, TEST_EMAIL
        )
        self.browser.find_element_by_id("password").send_keys(PASSWORD_TEST)
        self.browser.find_element_by_id("password2").send_keys(PASSWORD_TEST)
        self.browser.find_element_by_tag_name("button").click()

        # The account was created sucessfully and the page redirects 
        # Crane to home page
        self.wait_for(
            lambda *args: self.assertIn("W2W - What To Watch", 
                self.browser.title)
        )

        # Crane can see that he is now log in
        self.wait_to_be_logged_in(email=TEST_EMAIL)


    def test_login_and_signup(self):
        pass
