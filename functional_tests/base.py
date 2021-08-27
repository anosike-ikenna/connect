from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import unittest
from unittest import skip
import time

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_post_in_post_group(self, text_content, index):
        start_time = time.time()
        while True:
            try:
                posts = self.browser.find_elements_by_css_selector(".loadMore .central-meta")
                post_text_element = posts[index].find_element_by_css_selector(".description")
                self.assertIn(text_content, post_text_element.text)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)