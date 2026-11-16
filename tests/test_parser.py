from pathlib import Path
from unittest.mock import Mock
import unittest
import requests
from src.database import DatabaseRepository
from src.parser import ForumParser

FIXTURES = Path(__file__).parent / "fixtures"


class TestForumParser(unittest.TestCase):
    def setUp(self):
        self.parser = ForumParser()

    def test_parse_valid_fixture(self):
        html = (FIXTURES / "forum_page.html").read_text(encoding="utf-8")
        result = self.parser.parse_html(html)
        self.assertEqual([x["id"] for x in result], [101, 102, 103])
        self.assertEqual(result[0]["name"], "alice")
        self.assertIn("<b>форум</b>", result[0]["message"])

    def test_parse_invalid_fixture(self):
        html = (FIXTURES / "invalid_page.html").read_text(encoding="utf-8")
        result = self.parser.parse_html(html)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 202)

    def test_parse_page_mocked_request(self):
        html = (FIXTURES / "forum_page.html").read_text(encoding="utf-8")
        response = Mock(text=html)
        response.raise_for_status = Mock()
        session = Mock()
        session.get.return_value = response
        parser = ForumParser(session=session)
        result = parser.parse_page("https://example.org/thread")
        self.assertEqual(len(result), 3)
        session.get.assert_called_once_with("https://example.org/thread", headers=parser.HEADERS, timeout=10)
        self.assertIn("User-Agent", session.get.call_args.kwargs["headers"])

    def test_parse_page_network_error(self):
        session = Mock()
        session.get.side_effect = requests.Timeout("timeout")
        with self.assertRaises(requests.Timeout):
            ForumParser(session=session).parse_page("https://example.org/thread")

    def test_parse_page_http_error(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("404")
        session = Mock()
        session.get.return_value = response
        with self.assertRaises(requests.HTTPError):
            ForumParser(session=session).parse_page("https://example.org/thread")

    def test_parse_page_invalid_url(self):
        with self.assertRaises(ValueError):
            self.parser.parse_page("file:///tmp/page.html")

    def test_save_to_db_and_skip_duplicates(self):
        html = (FIXTURES / "forum_page.html").read_text(encoding="utf-8")
        data = self.parser.parse_html(html)
        with DatabaseRepository(":memory:") as db:
            self.assertEqual(self.parser.save_to_db(data, db), 3)
            self.assertEqual(self.parser.save_to_db(data, db), 0)
            self.assertEqual(len(db.get_by_name("alice")), 2)


if __name__ == "__main__":
    unittest.main()
