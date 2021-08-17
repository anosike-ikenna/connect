from selenium import webdriver
import unittest
import time


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
        post_button = browser.find_element_by_id("id_post_btn")
        post_button.click()
        time.sleep(1)
        new_post = browser.find_element_by_css_selector(".loadMore .central-meta")
        text_content = new_post.find_element_by_css_selector(".description")
        self.assertTrue(text_content.text == INPUT_TEXT)

        # There is still a textbox inviting her to add another item.
        # She enters 'Guess who's back?'
        self.fail("Finish the test!")

        # The page updates, and now shows both items

        # satisfied, she closes her browser
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()