from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
import time

User = get_user_model()


class MyTimeLineTest(FunctionalTest):

    def create_pre_authenticated_session(self, email, username):
        user = User.objects.create(email=email, username=username)
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

    def test_logged_in_users_timelines_are_saved_as_my_timelines(self):
        email = "alice@test.com"
        username = "alice"
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email, username)

        # Alice is a logged-in user
        self.create_pre_authenticated_session(email, username)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email, username)
