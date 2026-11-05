import unittest

from page_data import extract_page_data


class TestExtractPageData(unittest.TestCase):
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_main_paragraph_preferred(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main><p>Main paragraph.</p></main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(actual["first_paragraph"], "Main paragraph.")

    def test_extract_page_data_multiple_links_and_images(self):
        input_url = "https://crawler-test.com/blog/"
        input_body = """<html><body>
            <h1>Blog</h1>
            <a href="post1">One</a>
            <a href="https://other.com/page">Two</a>
            <a href="/top">Three</a>
            <img src="a.png">
            <img src="https://cdn.example.com/b.png">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(
            actual["outgoing_links"],
            [
                "https://crawler-test.com/blog/post1",
                "https://other.com/page",
                "https://crawler-test.com/top",
            ],
        )
        self.assertEqual(
            actual["image_urls"],
            [
                "https://crawler-test.com/blog/a.png",
                "https://cdn.example.com/b.png",
            ],
        )

    def test_extract_page_data_missing_elements(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><div>Nothing useful</div></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_empty_html(self):
        actual = extract_page_data("", "https://crawler-test.com")
        self.assertEqual(actual["heading"], "")
        self.assertEqual(actual["outgoing_links"], [])
        self.assertEqual(actual["image_urls"], [])

    def test_extract_page_data_ignores_tags_without_attributes(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <a>No href</a>
            <img alt="No src">
            <a href="/ok">OK</a>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(actual["outgoing_links"], ["https://crawler-test.com/ok"])
        self.assertEqual(actual["image_urls"], [])

    def test_extract_page_data_h2_fallback(self):
        input_body = "<html><body><h2>Sub</h2><p>Text</p></body></html>"
        actual = extract_page_data(input_body, "https://crawler-test.com")
        self.assertEqual(actual["heading"], "Sub")


if __name__ == "__main__":
    unittest.main()
