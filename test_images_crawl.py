import unittest

from images_crawl import get_images_from_html, get_urls_from_html


class TestGetURLsFromHTML(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = (
            "<html><body>"
            '<a href="/path/one">One</a>'
            '<a href="https://other.com/path/one">Other</a>'
            "</body></html>"
        )
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/path/one",
            "https://other.com/path/one",
        ]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_nested_and_relative_paths(self):
        input_url = "https://crawler-test.com/blog/"
        input_body = (
            "<html><body><div><p>"
            '<a href="post-1">Post</a>'
            '<a href="../about">About</a>'
            "</p></div></body></html>"
        )
        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/blog/post-1",
            "https://crawler-test.com/about",
        ]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_missing_href(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a name="x">No href</a><a href="/ok">OK</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/ok"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_anchors(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><p>Nothing here</p></body></html>"
        actual = get_urls_from_html(input_body, input_url)
        self.assertEqual(actual, [])


class TestGetImagesFromHTML(unittest.TestCase):
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://cdn.example.com/a.jpg" alt="A"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://cdn.example.com/a.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = (
            "<html><body>"
            '<img src="/logo.png" alt="Logo">'
            '<img src="images/banner.png">'
            '<img src="https://cdn.example.com/a.jpg">'
            "</body></html>"
        )
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/logo.png",
            "https://crawler-test.com/images/banner.png",
            "https://cdn.example.com/a.jpg",
        ]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="No src"><img src="/ok.png"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/ok.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_alt(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><p>No images</p></body></html>"
        actual = get_images_from_html(input_body, input_url)
        self.assertEqual(actual, [])


if __name__ == "__main__":
    unittest.main()
