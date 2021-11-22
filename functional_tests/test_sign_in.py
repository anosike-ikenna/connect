from django.core import mail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from .base import FunctionalTest
import re
import time

TEST_USERNAME = "alice123"
TEST_EMAIL = "alice@test.com"
SUBJECT = "your login link for connect"


class SignupTest(FunctionalTest):

    def test_can_get_email_link_to_sign_up_and_log_in(self):
        # Alice visits the connect site and wants to create
        # an account for hereself. She sees a user section.
        # She clicks on it and a dropdown appears, 
        # with one of the dropdown elements having a login
        # link. She clicks on it.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_css_selector("#auth-sec").click()
        self.wait_for_load(
            lambda: self.browser.find_element_by_id("signup-link")
        ).click()

        # She is taken away from the page to the signup page
        # Alice sees two input boxes inviting her to enter
        # first, her desired username, second, her valid email.
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector(
                ".reg input[name='username']"
            )
        ).send_keys(TEST_USERNAME)
        self.browser.find_element_by_css_selector(
            ".reg input[name='email']"
        ).send_keys(TEST_EMAIL)
        self.browser.find_element_by_css_selector(".signup").click()

        # A message appears telling her an email has been sent
        self.wait_for_load(
            lambda: self.assertIn(
                "check your email",
                self.browser.find_element_by_tag_name("body").text.lower()
            )
        )

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJECT, email.subject.lower())

        # It has a url link in it
        self.assertIn("use this link to log in", email.body.lower())
        url_search = re.search(r"http://.+/.+$", email.body.lower())
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)
        
        # She clicks it
        self.browser.get(url)

        # She sees the navbar of now has icons linking
        # to her messages and notifications
        self.assertTrue(
            self.wait_for_load(
                lambda: self.browser.find_element_by_id("user-noti")
            ).is_displayed()
        )
        self.assertTrue(
            self.browser.find_element_by_id("user-msgs").is_displayed()
        )

        # She decides to see what the site is all about by submitting a post
        self.add_timeline_post("Take me to the rooftop - billie eilish")

        # She clicks on the dropdown in the user section once again
        # she notices there is no longer signup and login buttons
        # But a logout button is now on display
        self.wait_to_be_logged_in(email=TEST_EMAIL, username=TEST_USERNAME)

        # Satisfied she closes her browser
        self.browser.quit()

        # She opens her browser and visits her favorite social
        # network, connect
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        # Alice tries use to connect's awesome log in page
        # to log in to her awesome account. She sees a
        # user section. she clicks on it and a dropdown appears,
        # with one of the dropdown elements having a login link.
        # she clicks on the login link
        self.browser.find_element_by_css_selector("#auth-sec").click()
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector("#login-link")
        ).click()

        # She is taken away from the page to a new page(login) having
        # an input box, invitiing her to enter her email
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector('.sign input[name="email"]')
        ).send_keys(TEST_EMAIL)
        self.browser.find_element_by_css_selector(
            ".sign input[name=email]").send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for_load(
            lambda: self.assertIn(
                "check your email",
                self.browser.find_element_by_tag_name("body").text.lower()
            )
        )
        
        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject.lower(), SUBJECT)

        # It has a url link in it
        self.assertIn("use this link to log in", email.body.lower())
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She sees the navbar of now has icons linking
        # to her messages and notifications
        self.assertTrue(
            self.wait_for_load(
                lambda: self.browser.find_element_by_id("user-noti")
            ).is_displayed()
        )
        self.assertTrue(
            self.browser.find_element_by_id("user-msgs").is_displayed()
        )

        # She clicks on the dropdown in the user section once again
        # she notices there is no longer signup and login buttons
        # But a logout button is now on display
        # She is logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL, username=TEST_USERNAME)

        # She logs out
        self.browser.find_element_by_id("logout-link").click()

        # She is logged out
        self.wait_to_be_logged_out(email=TEST_EMAIL, username=TEST_USERNAME)