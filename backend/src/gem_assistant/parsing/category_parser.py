"""Reads GeM's category search page (mkp.gem.gov.in/search?q=...): which categories a word falls in."""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser

QUADRANT_WARNING = {
    "Q1": "Q1: only the maker (OEM) can sell here.",
    "Q2": "Q2: you need the maker's authorisation to sell here.",
    "Q3": "Q3: open to any seller.",
}


@dataclass(frozen=True)
class Category:
    group: str
    name: str
    quadrant: str | None
    path: str

    @property
    def warning(self) -> str | None:
        return QUADRANT_WARNING.get(self.quadrant or "")


class _Reader(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.found: list[Category] = []
        self._group = ""
        self._in_strong = self._in_link = False
        self._href = ""
        self._text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "strong":
            self._in_strong, self._group = True, ""
        elif tag == "a" and ("/search" in (dict(attrs).get("href") or "")):
            self._in_link, self._href, self._text = True, dict(attrs)["href"], ""

    def handle_data(self, data):
        if self._in_strong:
            self._group += data
        elif self._in_link:
            self._text += data

    def handle_endtag(self, tag):
        if tag == "strong":
            self._in_strong = False
            self._group = self._group.strip()
        elif tag == "a" and self._in_link:
            self._in_link = False
            text = " ".join(self._text.split())
            match = re.search(r"\s*\((Q[123])\)$", text)
            name = text[:match.start()] if match else text
            if name and self._group:
                self.found.append(Category(self._group, name, match.group(1) if match else None,
                                           self._href.split("#")[0]))


def parse_categories(html: str) -> list[Category]:
    reader = _Reader()
    reader.feed(html)
    return reader.found
