from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
import time

User = get_user_model()


class MyTimeLineTest(FunctionalTest):

    def test_logged_in_users_timelines_are_saved_as_my_timelines(self):
        email = "alice@test.com"
        username = "alice"

        # Alice is a logged-in user
        self.create_pre_authenticated_session(email, username)
        self.browser.get(self.live_server_url)
        self.add_timeline_post("my very first post")
        self.add_timeline_post("my second post")
        feeds_url = self.browser.current_url

        # She notices a "Timeline" link for the first time
        self.browser.find_element_by_id("timeline-link").click()

        # She sees that her timeline is there, with each post
        # from newest to oldest
        self.wait_for_load(
            lambda: self.check_for_post_in_post_group("my second post", 0)
        )
        self.check_for_post_in_post_group("my very first post", 1)

        # She logs out. The 'timeline' option dissapears
        self.browser.find_element_by_css_selector("#auth-sec").click()
        self.wait_for_load(
            lambda: self.browser.find_element_by_id("logout-link")
        ).click()
        time.sleep(5)
