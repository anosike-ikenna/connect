from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import unittest
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    
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

    def test_can_make_a_text_post_for_one_user(self):
        # Alice checks out the homepage to the hottest social network site
        self.browser.get(self.live_server_url)

        # She notices the sleek page title contains the site name
        self.assertIn("Connect Social Network", self.browser.title)

        # she sees a textbox that invites her to 'write something'
        inputbox = self.browser.find_element_by_id("id_new_post")
        self.assertEqual(
            inputbox.get_attribute("placeholder").lower(), 
            "write something..."
        )

        # she types 'Hello everybody' into the textbox
        INPUT_TEXT = "Hello everybody"
        inputbox.send_keys(INPUT_TEXT)

        # when she hits post, the page updates and now contains
        # 'Hello everybody' and the timestamp
        post_button = self.browser.find_element_by_id("id_post_btn")
        post_button.click()
        self.check_for_post_in_post_group(INPUT_TEXT, 0)

        # There is still a textbox inviting her to write something.
        # She enters 'Guess who's back?'
        inputbox = self.browser.find_element_by_id("id_new_post")
        INPUT_TEXT2 = "Guess who's back?"
        inputbox.send_keys(INPUT_TEXT2)
        post_button = self.browser.find_element_by_id("id_post_btn")
        post_button.click()

        # The page updates, and now shows both items
        self.check_for_post_in_post_group(INPUT_TEXT2, 0)
        self.check_for_post_in_post_group(INPUT_TEXT, 1)

    def test_multiple_users_can_make_posts_at_different_urls(self):
        # Alice starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_post")
        inputbox.send_keys("Hello everybody")
        post_button = self.browser.find_element_by_id("id_post_btn")
        post_button.click()
        self.check_for_post_in_post_group("Hello everybody", 0)

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
        self.assertNotIn("Hello everybody", page_text)
        self.assertNotIn("Guess who's back?", page_text)

        # Nikki starts posting to his timeline.
        inputbox = self.browser.find_element_by_id("id_new_post")
        inputbox.send_keys("The return of ikenna")
        post_button = self.browser.find_element_by_id("id_post_btn")
        post_button.click()
        self.check_for_post_in_post_group("The return of ikenna", 0)

        # Nikki gets his own unique URL
        nikki_timeline_url = self.browser.current_url
        self.assertRegex(nikki_timeline_url, "/.+/timeline/")
        self.assertNotEqual(nikki_timeline_url, alice_timeline_url)
        
        # Again there is no trace of Alice's list
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Hello everybody", page_text)
        self.assertNotIn("Guess who's back?", page_text)
        