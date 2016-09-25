from . import base
from accounts.forms import (
    EMPTY_EMAIL_ERROR, EMPTY_PASSWORD_ERROR, EMPTY_PASSWORD2_ERROR,
    UNIQUE_EMAIL_ERROR, DIFFERENT_PASSWORDS_ERROR, INVALID_LOGIN_ERROR
)

from django.contrib.auth import get_user_model


User = get_user_model()


TEST_EMAIL = "crane@jago.com"
PASSWORD_TEST = "crane"
PASSWORD2_TEST = "crane2"


class SignUpLogInLogOutTest(base.FunctionalTest):

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
            lambda *args: self.assertIn("Create new account", 
                self.browser.title)
        )
        
        # Crane enters his email: crane@jago.com, passwords and hit post button
        self.browser.find_element_by_id("id_email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_id("id_password").send_keys(PASSWORD_TEST)
        self.browser.find_element_by_id("id_password2").send_keys(PASSWORD2_TEST)

        self.browser.find_element_by_id("id_submit").click()
        
        # The page informs him that given passwords do not mutch
        self.wait_for_element_with_class(".has-error")
        error = self.browser.find_elements_by_css_selector('.has-error')
        self.assertIn(DIFFERENT_PASSWORDS_ERROR, [ item.text for item in error])

        # Crane notices that email address he specified before is still there,
        # but passwords are gone.
        self.assertEqual(
            self.browser.find_element_by_id("id_email").get_attribute("value"),
            TEST_EMAIL
        )
        self.assertEqual(
            self.browser.find_element_by_id("id_password").get_attribute("value"),
            ""
        )
        self.assertEqual(
            self.browser.find_element_by_id("id_password2").get_attribute("value"),
            ""
        )

        # Crane enters correct passwords this time and press button. 
        self.browser.find_element_by_id("id_password").send_keys(PASSWORD_TEST)
        self.browser.find_element_by_id("id_password2").send_keys(PASSWORD_TEST)
        self.browser.find_element_by_id("id_submit").click()

        # The account was created sucessfully and the page redirects 
        # Crane to home page
        self.wait_for(
            lambda *args: self.assertIn("W2W - What To Watch", 
                self.browser.title)
        )

        # Crane can see that he is now log in
        self.wait_to_be_logged_in(email=TEST_EMAIL)


    def test_login_and_logout(self):
        # Crane has already created account on W2W
        User.objects.create(
            email = TEST_EMAIL, 
            password = PASSWORD_TEST
        )

        # He visitis his favourite webpage and looks for some movie to watch
        self.browser.get(self.server_url)

        # He notices Log In button in navbar and clicks it
        self.browser.find_element_by_id("id_login").click()

        # New site appears with title 'W2W - Log In', where 
        # he has to enter his email as well as password. 
        self.wait_for(
            lambda *args: self.assertIn("Log In", 
                self.browser.title)
        )

        # Crane enters his email: crane@jago.com, but wrong passwords
        self.browser.find_element_by_id("id_email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_id("id_password").send_keys(PASSWORD2_TEST)

        # The page informs him that given email address or password are invalid
        self.wait_for_element_with_class(".has-error")
        error = self.browser.find_elements_by_css_selector('.has-error')
        self.assertIn(INVALID_LOGIN_ERROR, [ item.text for item in error])

        # Crane enters correct passwords this time and press button. 
        self.browser.find_element_by_id("id_password").send_keys(PASSWORD_TEST)
        self.browser.find_element_by_id("id_submit").click()

        # The page redirects him to home page
        self.wait_for(
            lambda *args: self.assertIn("W2W - What To Watch", 
                self.browser.title)
        )

        # Crane can see that he is now log in
        self.wait_to_be_logged_in(email = TEST_EMAIL)

        # Howover he changes his mind and does not want to watch movie tonight.
        # He decided to log out.
        self.browser.find_element_by_id("id_logout").click()
        self.wait_to_be_logged_out(email = EMAIL_TEST)