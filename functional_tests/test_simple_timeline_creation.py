from .base import FunctionalTest
from selenium import webdriver
import time


class NewVisitorTest(FunctionalTest):

    def test_can_make_a_text_post_for_one_user(self):
        # Alice checks out the homepage to the hottest social network site
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

    def test_multiple_users_can_make_posts_at_different_urls(self):
        # Alice starts a new to-do list
        self.browser.get(self.live_server_url)
        self.add_timeline_post("hello everybody")

        # she notices that her timeline has a unique URL
        alice_timeline_url = self.browser.current_url
        self.assertRegex(alice_timeline_url, "/.+/timeline/")

        # Now a new user, Nikki, comes along to the site.

        ## I use a new browser session to make sure that no information
        ## of Alice is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Nikki visits the home page. There is no sign of Alice's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        # self.assertNotIn("Hello everybody", page_text)  #*******To be fixed*******#
        # self.assertNotIn("Guess who's back?", page_text)    #**********To be fixed*********#

        # Nikki starts posting to his timeline.
        self.add_timeline_post("the return of ikenna")

        # Nikki gets his own unique URL
        nikki_timeline_url = self.browser.current_url
        self.assertRegex(nikki_timeline_url, "/.+/timeline/")
        self.assertNotEqual(nikki_timeline_url, alice_timeline_url)
        
        # Again there is no trace of Alice's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Hello everybody", page_text)
        self.assertNotIn("Guess who's back?", page_text)