import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        actual = normalize_url("https://www.boot.dev/blog/path")
        self.assertEqual(actual, "www.boot.dev/blog/path")

    def test_trailing_slash(self):
        actual = normalize_url("https://www.boot.dev/blog/path/")
        self.assertEqual(actual, "www.boot.dev/blog/path")

    def test_http_and_https_match(self):
        self.assertEqual(
            normalize_url("http://www.boot.dev/blog/path"),
            normalize_url("https://www.boot.dev/blog/path"),
        )

    def test_uppercase_host(self):
        actual = normalize_url("https://WWW.Boot.DEV/blog/path")
        self.assertEqual(actual, "www.boot.dev/blog/path")

    def test_path_case_preserved(self):
        actual = normalize_url("https://www.boot.dev/Blog/Path")
        self.assertEqual(actual, "www.boot.dev/Blog/Path")

    def test_query_string_removed(self):
        actual = normalize_url("https://www.boot.dev/blog/path?utm=x&a=1")
        self.assertEqual(actual, "www.boot.dev/blog/path")

    def test_fragment_removed(self):
        actual = normalize_url("https://www.boot.dev/blog/path#section-2")
        self.assertEqual(actual, "www.boot.dev/blog/path")

    def test_root_path(self):
        self.assertEqual(normalize_url("https://boot.dev/"), "boot.dev")
        self.assertEqual(normalize_url("https://boot.dev"), "boot.dev")

    def test_no_scheme(self):
        actual = normalize_url("www.boot.dev/blog/path")
        self.assertEqual(actual, "www.boot.dev/blog/path")

    def test_port_kept(self):
        actual = normalize_url("http://localhost:8080/a/b/")
        self.assertEqual(actual, "localhost:8080/a/b")

    def test_surrounding_whitespace(self):
        actual = normalize_url("  https://www.boot.dev/blog/path  ")
        self.assertEqual(actual, "www.boot.dev/blog/path")


if __name__ == "__main__":
    unittest.main()
