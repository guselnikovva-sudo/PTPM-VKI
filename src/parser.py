"""Parser for a documented forum HTML layout."""
import re
import requests
from bs4 import BeautifulSoup


class ForumParser:
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; LabForumParser/1.0; educational project)", "Accept": "text/html,application/xhtml+xml"}

    def __init__(self, timeout=10, session=None):
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.timeout = timeout
        self.session = session if session is not None else requests.Session()

    @staticmethod
    def parse_html(html: str) -> list[dict]:
        if not isinstance(html, str):
            raise TypeError("html must be a string")
        soup = BeautifulSoup(html, "lxml")
        comments = []
        seen = set()
        for post in soup.select("article.comment, div.comment"):
            raw_id = post.get("data-comment-id") or post.get("id", "")
            match = re.fullmatch(r"(?:comment-|post-)?([1-9][0-9]*)", str(raw_id))
            author = post.select_one(".author, .username")
            body = post.select_one(".message, .post-content")
            if not match or author is None or body is None:
                continue
            comment_id = int(match.group(1))
            if comment_id in seen:
                continue
            username = author.get_text(" ", strip=True)
            message = body.decode_contents().strip()
            if not username or not message:
                continue
            comments.append({"id": comment_id, "name": username, "message": message})
            seen.add(comment_id)
        return comments

    def parse_page(self, url: str) -> list[dict]:
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")
        response = self.session.get(url, headers=self.HEADERS, timeout=self.timeout)
        response.raise_for_status()
        return self.parse_html(response.text)

    @staticmethod
    def save_to_db(parsed_data, repository) -> int:
        """Return count of inserted comments; skip already-existing IDs."""
        inserted = 0
        for comment in parsed_data:
            if repository.get_by_id(comment["id"]) is not None:
                continue
            repository.add(comment["id"], comment["name"], comment["message"])
            inserted += 1
        return inserted
