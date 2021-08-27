from .base import FunctionalTest
from unittest import skip
import time


class PostValidationTest(FunctionalTest):
    
    @skip
    def test_cannot_add_empty_list_items(self):
        # Alice goes to the home page and accidentally tries to submit
        # an empty post. She hits enter on the empty input box.

        # The home page refreshes, and there is an error page saying
        # that a post cannot be blank

        # She tries again with some text for the post, which now works

        # Pervesely, she now decides to submit a second blank list item

        # She recieves a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail("write me")