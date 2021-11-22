from django.conf import settings
from .base import FunctionalTest
from selenium import webdriver
import time
import os


class NewVisitorTest(FunctionalTest):

    def test_can_make_a_text_post_for_one_user(self):
        email = "alice@test.com"
        username = "alice"
        # Alice checks out the homepage to the hottest social network site
        self.create_pre_authenticated_session(email=email, username=username)
        self.browser.get(self.live_server_url)

        # She notices the sleek page title contains the site name
        self.assertIn("Connect Social Network", self.browser.title)

        # she sees a textbox that invites her to 'write something'
        inputbox = self.get_post_input_box()
        self.assertEqual(
            inputbox.get_attribute("placeholder").lower(), 
            "write something..."
        )

        # she types 'Hello everybody' into the textbox
        INPUT_TEXT = "Hello everybody"
        inputbox.send_keys(INPUT_TEXT)

        # when she hits post, the page updates and now contains
        # 'Hello everybody' and the timestamp
        post_button = self.get_post_submit_button()
        post_button.click()
        self.check_for_post_in_post_group(INPUT_TEXT, 0)

        # There is still a textbox inviting her to write something.
        # She enters 'Guess who's back?'
        inputbox = self.get_post_input_box()
        INPUT_TEXT2 = "Guess who's back?"
        inputbox.send_keys(INPUT_TEXT2)
        post_button = self.get_post_submit_button()
        post_button.click()

        # The page updates, and now shows both items
        self.check_for_post_in_post_group(INPUT_TEXT2, 0)
        self.check_for_post_in_post_group(INPUT_TEXT, 1)

    def test_multiple_users_can_make_posts_at_same_url(self):
        # Alice starts a new post
        email1, username1 = "alice@test.com", "alice"
        email2, username2 = "nikki@test.com", "nikki"

        self.create_pre_authenticated_session(email=email1, username=username1)
        self.browser.get(self.live_server_url)
        self.add_timeline_post("hello everybody")

        # she has her own unique session id
        alice_session_id = self.browser.get_cookie(settings.SESSION_COOKIE_NAME)["value"]
        self.assertIsNotNone(alice_session_id)

        # Now a new user, Nikki, comes along to the site.

        ## I use a new browser session to make sure that no information
        ## of Alice is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Nikki visits the home page. There is no sign of Alice's list
        self.create_pre_authenticated_session(email=email2, username=username2)
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        # self.assertNotIn("Hello everybody", page_text)  #*******To be fixed*******#
        # self.assertNotIn("Guess who's back?", page_text)    #**********To be fixed*********#

        # Nikki starts posting to his timeline.
        self.add_timeline_post("the return of ikenna")

        # Nikki gets his own unique session id
        nikki_session_id = self.browser.get_cookie(settings.SESSION_COOKIE_NAME)["value"]
        self.assertIsNotNone(nikki_session_id)
        self.assertNotEqual(nikki_session_id, alice_session_id)
        
        # Again there is no trace of Alice's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Hello everybody", page_text)
        self.assertNotIn("Guess who's back?", page_text)

    def test_post_can_include_a_file(self):
        email1, username1 = "alice@test.com", "alice"
        email2, username2 = "nikki@test.com", "nikki"
        TEST_IMG = os.path.abspath("c:/users/ikenna/pictures/test2.jpg")
        self.assertTrue(os.path.exists(TEST_IMG))

        # Alice logs on to her awesome connect account
        self.create_pre_authenticated_session(email=email1, username=username1)
        self.browser.get(self.live_server_url)

        # She decides to make a post containing an image of herself
        inputbox = self.get_post_input_box()
        inputbox.send_keys("first post")

        img_file_input = self.browser.find_element_by_id("file-upload")
        img_file_input.send_keys(TEST_IMG)
        inputbox.submit()

        # she is taken to her timeline where she sees her post with her image
        posts = self.browser.find_elements_by_css_selector(".loadMore .central-meta")
        post_text_element = posts[0].find_element_by_css_selector(".description")
        self.assertIn("first post", post_text_element.text)
        self.assertTrue(posts[0].find_element_by_css_selector(".post_img").is_displayed())