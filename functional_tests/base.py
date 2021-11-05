from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
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

    def wait_for_load(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_post_input_box(self):
        return self.browser.find_element_by_id("id_new_post")

    def get_post_submit_button(self):
        return self.browser.find_element_by_id("id_post_btn")

    def wait_to_be_logged_in(self, email, username):
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector("#auth-sec")
        ).click()
        self.assertTrue(
            self.wait_for_load(
                lambda: self.browser.find_element_by_id("logout-link")
            ).is_displayed()
        )
        for id in ["signup-link", "login-link"]:
            with self.assertRaises(NoSuchElementException):
                self.browser.find_element_by_id(id)

    def wait_to_be_logged_out(self, email, username):
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector("#auth-sec")
        ).click()
        with self.assertRaises(NoSuchElementException):
            self.wait_for_load(
                lambda: self.browser.find_element_by_id("logout-link")
            )
        self.browser.find_element_by_css_selector("#login-link")