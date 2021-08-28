from .base import FunctionalTest
from unittest import skip
import time


class PostValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        # Alice goes to the home page and accidentally tries to submit
        # an empty post. She hits enter on the empty input box.
        self.browser.get(self.live_server_url)
        self.get_post_submit_button().click()

        # The home page refreshes, and there is an error page saying
        # that a post cannot be blank
        self.wait_for_load(
            lambda: self.assertEqual(
                self.browser.find_element_by_id("post_error").text.lower(),
                "you can't have an empty post"
            )
        )

        # She tries again with some text for the post, which now works
        self.get_post_input_box().send_keys("Hello friend")
        self.get_post_submit_button().click()
        self.check_for_post_in_post_group("Hello friend", 0)


        # Pervesely, she now decides to submit a second blank list 
        self.get_post_submit_button().click()

        # She recieves a similar warning on the list page
        self.wait_for_load(
            lambda: self.assertEqual(
                self.browser.find_element_by_id("post_error").text.lower(),
                "you can't have an empty post"
            )
        )

        # And she can correct it by filling some text in
        self.get_post_input_box().send_keys("Life sucks")
        self.get_post_submit_button().click()
        self.check_for_post_in_post_group("Hello friend", 1)
        self.check_for_post_in_post_group("Life sucks", 0)