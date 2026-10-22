"""Step 3.5: a bid's allowed specification values against his main products' key specs. A review, never a block."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from gem_assistant.domain.models import (
    BidAnalysis, Evidence, ExtractionMethod, ProductSpec, SellerProfile, SpecRow,
)
from gem_assistant.eligibility.rules import DEFAULT_RULES, SpecMatchRule, spec_allows
from gem_assistant.infrastructure.pypdf_extractor import PypdfTextExtractor
from gem_assistant.parsing.label_extractor import LabelFieldExtractor
from gem_assistant.parsing.spec_table import read_specifications

AT = datetime(2026, 10, 22, tzinfo=timezone.utc)
FIX = Path(__file__).parent / "fixtures"


def _analyse(name: str) -> BidAnalysis:
    data = (FIX / name).read_bytes()
    pages = PypdfTextExtractor(300).extract(data)
    return BidAnalysis(bid_number="GEM/2026/B/1", source_name=name, sha256="a" * 64, page_count=len(pages),
                       unread_lines=0, imported_at=AT, fields=LabelFieldExtractor().extract(pages), flags=[],
                       specifications=read_specifications(data, pages))


def _run(bid, *products):
    return SpecMatchRule().evaluate(bid, SellerProfile(products=list(products)), AT)


@pytest.mark.parametrize("allowed, mine, expected", [
    ("Black", "black", True), ("Black", "Magenta", False),
    ("Brown, White", " white ", True), ("Canon - PFI-8110 BK", "PFI-8110 BK", True),
    ("1, 2, 3, 4, 5 Or higher", "7", True), ("1, 2, 3, 4, 5 Or higher", "0", False),
    ("1001 to 2000, 2001 to 5000", "1500", True), ("1001 to 2000, 2001 to 5000", "5001", False),
    ("1200 mm", "1200", True), ("1200 mm", "1000", False),
    ("1, 2, 3", "two years", None),  # a text value against numbers: cannot be compared, so not a mismatch
])
def test_allowed_values_are_matched_as_words_lists_numbers_and_bands(allowed, mine, expected):
    assert spec_allows(allowed, mine) is expected


def test_real_cartridge_bid_with_a_wrong_colour_is_one_review_quoting_the_closest_table():
    bid = _analyse("GEM-2026-B-8142835_doc10014519.pdf")  # 4 tables: Black, Magenta, Cyan, Yellow
    (r,) = _run(bid, ProductSpec(name="Ink Cartridges", specs={"Color of the Ink/Toner": "Red", "Type of Cartridge/Consumable": "ink cartridge"}))
    assert r.outcome.value == "NEEDS_REVIEW" and r.evidence.page in {3, 4, 5, 6}
    assert "Your product “Ink Cartridges” has Color of the Ink/Toner = Red" in r.reason
    assert "Offer a product that matches exactly" in r.reason


def test_silent_when_any_table_fits_or_nothing_can_be_compared():
    bid = _analyse("GEM-2026-B-8142835_doc10014519.pdf")
    assert _run(bid, ProductSpec(name="Ink Cartridges", specs={"Color of the Ink/Toner": "Magenta"})) == []  # one table fits
    assert _run(bid, ProductSpec(name="Ink Cartridges", specs={"Nothing Like It": "x"})) == []
    assert _run(bid, ProductSpec(name="Laptop", specs={"Color of the Ink/Toner": "Red"})) == []  # not this item
    assert SpecMatchRule().evaluate(bid, None, AT) == []
    assert _run(_analyse("GEM-2026-B-8105558_doc9971825.pdf"), ProductSpec(name="Laptop", specs={"RAM": "4"})) == []


def test_real_office_bid_flags_a_wrong_table_top_and_never_blocks():
    bid = _analyse("GEM-2026-B-8054438_doc9913333.pdf")
    results = _run(bid, ProductSpec(name="Revolving Chair", specs={"Type of system": "Wall based"}),  # no table has it: silent
                   ProductSpec(name="Modular Work Stations", specs={"Material of table top": "Glass"}))  # both tables allow Particle Board
    assert [r.outcome.value for r in results] == ["NEEDS_REVIEW"] and "Modular Work Stations" in results[0].reason
    assert SpecMatchRule in {type(r) for r in DEFAULT_RULES}
