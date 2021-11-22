from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from main.models import TimeLine
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import unittest
from unittest import skip
import time

User = get_user_model()
MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def create_pre_authenticated_session(self, email, username):
        user = User.objects.create(email=email, username=username)
        TimeLine.objects.create(user=user)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.create()
        ## To set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path="/"
        ))

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

    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn

    @wait
    def wait_for_load(self, fn):
        return fn()

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

    def add_timeline_post(self, post_text):
        self.get_post_input_box().send_keys(post_text)
        self.get_post_submit_button().click()
        self.check_for_post_in_post_group(post_text, 0)