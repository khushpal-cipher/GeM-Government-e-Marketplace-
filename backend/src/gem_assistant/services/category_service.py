"""Looks up GeM's category names for a search word (step 4.1), one public page per word."""

from __future__ import annotations

import re
from urllib.parse import quote

from ..parsing.category_parser import Category, parse_categories
from ..safety.safe_fetcher import SafeFetcher
from ..safety.response_classifier import Expect

SEARCH_URL = "https://mkp.gem.gov.in/search?q={word}"
_INVALID = re.compile(r"[~`!#$%\^*@+=\\\[\];{}|\":<>?]")  # same rule as the GeM search box


class CategoryService:
    def __init__(self, fetcher: SafeFetcher):
        self._fetcher = fetcher

    def lookup(self, word: str) -> list[Category]:
        word = " ".join(word.split())
        if not word or len(word) > 60 or _INVALID.search(word):
            raise ValueError("Use plain words (letters, numbers, spaces).")
        response = self._fetcher.get(SEARCH_URL.format(word=quote(word)), expect=Expect.CATEGORY_PAGE)
        return parse_categories(response.body.decode("utf-8", errors="replace"))
