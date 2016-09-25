from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import get_user_model

import sys
import time


User = get_user_model()


class FunctionalTest(StaticLiveServerTestCase):


    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url


    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()


    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def create_pre_authenticated_session(self, email, password):
        user = User.objects.create(email = email, password = password)
        session = SessionStore()
        session[SESSION_KEY] = user.pk #1
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key, #2
            path='/',
        ))

    def wait_for_movies_list_update(self, retries = 60):
        while retries > 0:
            state_msg = self.browser.find_element_by_id("state-msg")
            if state_msg.text == "" or not state_msg.is_displayed():
                return
            retries -= 1
            time.sleep(0.5)
        self.fail("could not wait longer for state-msg to disappear")


    def wait_for(self, function_with_assertion, timeout = 10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        # one more try, which will raise any errors if they are outstanding
        return function_with_assertion()


    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout = 10).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )


    def wait_for_element_with_class(self, class_name, timeout = 10):
        WebDriverWait(self.browser, timeout = timeout).until(
            lambda b: b.find_element_by_css_selector(class_name),
            "Could not find element with class {}. Page text was:\n{}".format(
                class_name, self.browser.find_element_by_tag_name("body").text)
            )


    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)


    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)