import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_https_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http_trailing_slash(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_heading_from_html(self):
        html = "<html><body><h1>Hello, World!</h1></body></html>"
        actual = get_heading_from_html(html)
        expected = "Hello, World!"
        self.assertEqual(actual, expected)

    def test_heading_from_html_h2(self):
        html = "<html><body><h2>Hello from H2!</h2></body></html>"
        actual = get_heading_from_html(html)
        expected = "Hello from H2!"
        self.assertEqual(actual, expected)

    def test_heading_from_html_no_heading(self):
        html = "<html><body><p>Just some text</p></body></html>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_heading_from_html_prefers_h1(self):
        html = "<html><body><h1>H1 title</h1><h2>H2 title</h2></body></html>"
        actual = get_heading_from_html(html)
        expected = "H1 title"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_basic(self):
        html = "<html><body><p>Hello paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(html)
        expected = "Hello paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_main_priority(self):
        html = """
        <html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>
        """
        actual = get_first_paragraph_from_html(html)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_none(self):
        html = "<html><body><h1>Title</h1></body></html>"
        actual = get_first_paragraph_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'

        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]

        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/"><span>Boot.dev</span></a></body></html>'

        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/"]

        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """
            <html>
                <body>
                    <a href="/one">One</a>
                    <a href="/two">Two</a>
                    <a href="https://example.com/three">Three</a>
                </body>
            </html>
        """

        actual = get_urls_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/one",
            "https://crawler-test.com/two",
            "https://example.com/three",
        ]

        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://example.com/cat.png"></body></html>'

        actual = get_images_from_html(input_body, input_url)
        expected = ["https://example.com/cat.png"]

        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img alt="A cat"></body></html>'

        actual = get_images_from_html(input_body, input_url)
        expected = []

        self.assertEqual(actual, expected)

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


if __name__ == "__main__":
    unittest.main()
