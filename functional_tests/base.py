from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

import sys
import time

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

    def wait_for_movies_list_update(self, retries = 60):
        while retries > 0:
            state_msg = self.browser.find_element_by_id("state-msg")
            if state_msg.text == "" or not state_msg.is_displayed():
                return
            retries -= 1
            time.sleep(0.5)
        self.fail("could not wait longer for state-msg to disappear")