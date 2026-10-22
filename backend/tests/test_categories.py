"""Step 4.1: category names and quadrant from the mkp search page (fixture seen 22 Oct 2026)."""

from pathlib import Path

import pytest

from gem_assistant.domain.ports import HttpResponse
from gem_assistant.parsing.category_parser import parse_categories
from gem_assistant.safety.response_classifier import Expect, ResponseClassifier, ResponseKind

HTML = (Path(__file__).parent / "fixtures" / "mkp-search-laptop_2026-10-22.html").read_text()


def test_reads_groups_names_and_quadrants():
    found = parse_categories(HTML)
    assert [(c.group, c.name, c.quadrant) for c in found] == [
        ("Computers", "High End Laptop - Notebook", "Q2"),
        ("Computers", "Rugged Notebook - Laptop", "Q2"),
        ("Computers", "Mobile Computer Workstation (V2)", "Q2"),
        ("Chassis Components", "Laptop Docking Station", "Q3"),
        ("Business Cases", "Office Bags (V2)", "Q3"),
        ("Business Cases", "Invented Q1 Item", "Q1"),
    ]
    assert found[0].path == "/computers-high-end-laptop-notebook/search"


def test_quadrant_warnings():
    by_name = {c.name: c for c in parse_categories(HTML)}
    assert "authorisation" in by_name["Rugged Notebook - Laptop"].warning
    assert "maker" in by_name["Invented Q1 Item"].warning


def _classify(body: str) -> ResponseKind:
    return ResponseClassifier().classify(HttpResponse("https://mkp.gem.gov.in/search", 200, {}, body.encode()), Expect.CATEGORY_PAGE).kind


def test_real_page_with_captcha_in_scripts_is_not_a_block():
    assert "captcha" in HTML.lower()
    assert _classify(HTML) is ResponseKind.OK


def test_challenge_page_is_still_a_block():
    assert _classify("<html><body>Please solve the captcha</body></html>") is ResponseKind.BLOCK


class _Fetcher:
    def __init__(self):
        self.urls = []

    def get(self, url, expect):
        self.urls.append((url, expect))
        return HttpResponse("https://mkp.gem.gov.in/search", 200, {}, HTML.encode())


def test_lookup_fetches_one_public_url():
    from gem_assistant.services.category_service import CategoryService
    fetcher = _Fetcher()
    assert len(CategoryService(fetcher).lookup("  laptop  bag ")) == 6
    assert fetcher.urls == [("https://mkp.gem.gov.in/search?q=laptop%20bag", Expect.CATEGORY_PAGE)]


@pytest.mark.parametrize("word", ["", "a<b", "x" * 61])
def test_lookup_refuses_bad_words(word):
    from gem_assistant.services.category_service import CategoryService
    with pytest.raises(ValueError):
        CategoryService(_Fetcher()).lookup(word)
