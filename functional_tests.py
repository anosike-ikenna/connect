from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_make_a_text_post(self):
        # Alice checks out the homepage to the hottest social network site
        self.browser.get("http://localhost:8000")

        # She notices the sleek page title contains the site name
        self.assertIn("Connect Social Network", self.browser.title)
        self.fail("Finish the test!")

        # she sees a textbox that invites her to 'write something'

        # she types 'Hello everybody' into the textbox

        # when she hits post, the page updates and now contains
        # 'Hello everybody' and the timestamp

        # There is still a textbox inviting her to add another item.
        # She enters 'Guess who's back?'

        # The page updates, and now shows both items

        # satisfied, she closes her browser
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()