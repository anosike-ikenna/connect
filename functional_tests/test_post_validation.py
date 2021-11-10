from .base import FunctionalTest
from unittest import skip
import time


class PostValidationTest(FunctionalTest):
    
    def test_cannot_add_empty_list_items(self):
        email = "alice@test.com"
        username = "alice"
        # Alice goes to the home page and accidentally tries to submit
        # an empty post. She hits enter on the empty input box.
        self.create_pre_authenticated_session(email=email, username=username)
        self.browser.get(self.live_server_url)
        self.get_post_submit_button().click()

        # The browser intercepts the request, and does not load the
        # homepage
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector(
                "#id_new_post:invalid"
            )
        )

        # She starts typing some text for the new item and the error dissapears
        self.get_post_input_box().send_keys("Hello my gee")
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector(
                "#id_new_post:valid"
            )
        )

        # And she can submit it successfully
        self.get_post_submit_button().click()
        self.check_for_post_in_post_group("Hello my gee", 0)

        # Perversely, she now decides to submit a second blank list item
        self.get_post_submit_button().click()

        # Again, the browser will not comply
        self.check_for_post_in_post_group("Hello my gee", 0)
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector(
                "#id_new_post:invalid"
            )
        )

        # And she can correct it by filling some text in
        self.get_post_input_box().send_keys("What's going on")
        self.wait_for_load(
            lambda: self.browser.find_element_by_css_selector(
                "#id_new_post:valid"
            )
        )
        self.get_post_submit_button().click()
        self.check_for_post_in_post_group("Hello my gee", 1)
        self.check_for_post_in_post_group("What's going on", 0)