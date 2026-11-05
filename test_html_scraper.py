import unittest

from html_scraper import get_first_paragraph_from_html, get_heading_from_html


class TestGetHeadingFromHtml(unittest.TestCase):
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self):
        input_body = "<html><body><h2>Subtitle</h2><p>Text</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Subtitle"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h1_priority_over_h2(self):
        input_body = """<html><body>
            <h2>Secondary</h2>
            <h1>Primary</h1>
        </body></html>"""
        actual = get_heading_from_html(input_body)
        expected = "Primary"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_heading(self):
        input_body = "<html><body><p>No headings here.</p></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_empty_string(self):
        self.assertEqual(get_heading_from_html(""), "")

    def test_get_heading_from_html_nested_tags_and_whitespace(self):
        input_body = "<h1>  Hello <em>brave</em> world  </h1>"
        actual = get_heading_from_html(input_body)
        expected = "Hello brave world"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_only_first_h1(self):
        input_body = "<h1>First</h1><h1>Second</h1>"
        self.assertEqual(get_heading_from_html(input_body), "First")


class TestGetFirstParagraphFromHtml(unittest.TestCase):
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = """<html><body>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self):
        input_body = "<html><body><h1>Title</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_without_paragraph_falls_back(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main><div>No paragraph in main.</div></main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_nested_tags(self):
        input_body = "<main><p>Some <a href='#'>linked</a> text.</p></main>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "Some linked text."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_empty_string(self):
        self.assertEqual(get_first_paragraph_from_html(""), "")


if __name__ == "__main__":
    unittest.main()
